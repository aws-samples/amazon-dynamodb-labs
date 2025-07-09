// show the query modal
function showQuery(caller) {
    initQuery();

    $("#selectQuery").show();
    $("#queryDiv").show();
}

// reset the query modal
function initQuery() {
    if (!model.DataModel) return;
    var name = model.DataModel[modelIndex].TableName;

    $(".remove").remove();
    $("#selectQuery").val($("#selectQuery option:first").val());
    $("#selectTableOrIndex").val($("#selectTableOrIndex option:first").val());
    $("#selectOp").val($("#selectOp option:first").val());
    $("#filterOp").val($("#filterOp option:first").val());
    $("#selectAttrType").val($("#selectAttrType option:first").val());

    $("#txtQueryName").val("");
    $("#txtPKval").val("");
    $("#txtSKval").val("");
    $("#txtSKendVal").val("");
    $("#txtFilterAttr").val("");
    $("#txtFilterValue").val("");
    $("#txtFilterEndValue").val("");
    $("#btnAddFilter").hide();
    $("#btnAddSort").hide();
    $("#queryConditions").css("display", "none");
    $("#skDiv").css("display", "none");
    $("#filterArea").css("display", "none");
    $("#queryDiv").hide();

    match_data = [];
    loadDataModel();

    $("#selectTableOrIndex").append(`<option value="${name}" class="remove">${name}</option>`);
    $.each(model.DataModel[modelIndex].GlobalSecondaryIndexes, function (idx, gsi) {
        $("#selectTableOrIndex").append(`<option value="${gsi.IndexName}" class="remove">${gsi.IndexName}</option>`)
    });

    $.each(datamodel.SavedQuery, function (name, query) {
        $("#selectQuery").append(`<option value="${name}" class="remove">${name}</option>`)
    });
    $("#selectQuery").append(`<option value="new" class="remove">Define new query...</option>`);
}

// show second value textbox if this is a between
function setOp(type) {
    if (type == 'sort') {
        if ($("#selectOp").val() == 'between') {
            $("#lblSKendVal").css("visibility", "visible");
            $("#txtSKendVal").css("visibility", "visible");
        } else {
            $("#lblSKendVal").css("visibility", "hidden");
            $("#txtSKendVal").css("visibility", "hidden");
        }
    } else {
        $.each($(".filterOp"), function (idx, select) {
            if (select.value == 'between') {
                $("#lblFilterEndVal" + select.id.substring(8)).css("visibility", "visible");
                $("#txtFilterEndVal" + select.id.substring(8)).css("visibility", "visible");
            } else {
                $("#lblFilterEndVal" + select.id.substring(8)).css("visibility", "hidden");
                $("#txtFilterEndVal" + select.id.substring(8)).css("visibility", "hidden");
            }
        });
    }
}

// make the sort condition area visible
function addSortCondition() {
    $("#btnAddSort").hide();
    $("#skDiv").show();
}

// add a filter to the query modal
function addFilter() {
    if ($("#filterArea").is(":hidden")) {
        numFilters = 0;
        $("#filterArea").show();
    }
    else {
        var clone = $("#filterDiv").clone(true);
        clone.attr("id", "filterDiv" + numFilters);
        clone.attr("class", "filterDiv remove");
        $("#selectFilter").append(clone);
        $("#filterDiv" + numFilters).find(">:first-child").show();

        $.each($("#filterDiv" + numFilters).children(), function (idx, child) {
            child.id = child.id + numFilters;
        });

        $("#selectFilter" + numFilters).val($("#selectFilter" + numFilters + " option:first").val());
        $("#selectAttrType" + numFilters).val($("#selectAttrType" + numFilters + " option:first").val());
        $("#txtFilterVal" + numFilters).val("");
        $("#txtFilterEndVal" + numFilters).val("");
        $("#txtFilterAttr" + numFilters).val("");

        $("#lblFilterEndVal" + numFilters).css("visibility", "hidden");
        $("#txtFilterEndVal" + numFilters).css("visibility", "hidden");

        numFilters++;
    }

    $("#selectFilter").scrollTop($("#selectFilter")[0].scrollHeight);
}

// create a query object
function buildQuery() {
    var query = {},
        test = {};

    query.view = $("#selectTableOrIndex").val();
    query.PK = $("#txtPKval").val();
    if ($("#selectOp").val() != null) {
        query.SK = {};
        query.SK.condition = $("#selectOp").val();
        query.SK.values = [];
        query.SK.values.push($("#txtSKval").val());

        if ( query.SK.condition == "between" )
            query.SK.values.push($("#txtSKendVal").val());
    }

    query.filter = [];

    $.each($(".filterDiv"), function (count, div) {
        if (!$("#filterArea").is(":visible"))
            return;

        var divId = count > 0 ? count - 1 : "";

        if (divId >= 0)
            test.operator = $("#selectAndOr" + divId).val();

        test.attribute = $("#txtFilterAttr" + divId).val();
        test.type = $("#selectAttrType" + divId).val();
        test.condition = $("#filterOp" + divId).val();
        test.values = [];
        test.values.push($("#txtFilterVal" + divId).val());

        if (test.condition == "between")
            test.values.push($("#txtFilterEndVal" + divId).val());

        query.filter.push(test);
        test = {};
    });

    if (!datamodel.hasOwnProperty("SavedQuery"))
        datamodel.SavedQuery = {};

    if ($("#txtQueryName").val() != "")
        datamodel.SavedQuery[$("#txtQueryName").val()] = query;

    runQuery($("#txtQueryName").val());
}

// load a query object into the query modal
function setConditions() {
    var query = $("#selectQuery").val();

    $("#selectQuery").css("display", "none");

    $("#queryConditions").show();
    $("#btnAddFilter").show();
    $("#btnAddSort").show();

    if (query == "new") {
        $("#lblQueryName").show();
        $("#txtQueryName").show();
        return;
    }

    $("#txtQueryName").val(query);
    query = datamodel.SavedQuery[query];
    $("#selectTableOrIndex").val(query.view);
    $("#txtPKval").val(query.PK);

    if (query.hasOwnProperty("SK")) {
        $("#skDiv").show();
        $("#btnAddSort").hide();
        $("#selectOp").val(query.SK.condition);
        $("#txtSKval").val(query.SK.values[0]);

        $("#txtSKendVal").css("display", "none");

        if (query.SK.condition == "between") {
            $("#txtSKendVal").val(query.SK.values[1]);
            $("#txtSKendVal").show();
        }
    }

    $.each(query.filter, function (idx, test) {
        var divId = idx > 0 ? idx - 1 : "";
        addFilter();

        if (divId != "")
            $("#selectAndOr" + divId).val(test.operator);

        $("#txtFilterAttr" + divId).val(test.attribute);
        $("#selectAttrType" + divId).val(test.type);
        $("#filterOp" + divId).val(test.condition);
        $("#txtFilterVal" + divId).val(test.values[0]);

        if (test.condition == "between")
            $("#txtFilterEndVal" + divId).val(test.values[1]);
    });
}

// execute the query and display the result
function runQuery(name) {
    var query = datamodel.SavedQuery[name],
        PK = "",
        SK = "";

    match_data = [];
    json_data = datamodel.TableData;

    if (query.view == datamodel.TableName) {
        PK = table.partition_key;
        SK = table.sort_key
    } else {
        $.each(datamodel.GlobalSecondaryIndexes, function (idx, gsi) {
            if (gsi.IndexName == query.view) {
                PK = gsi.KeyAttributes.PartitionKey.AttributeName;
                SK = gsi.KeyAttributes.SortKey.AttributeName;
                return false;
            }
        });
    }

    $.each(json_data, function (idx, item) {
        if (item.hasOwnProperty(PK) && getValue(item[PK]) == query.PK) {
            var test = {},
                pass = true;

            // test the sort condition if there is one
            if (query.hasOwnProperty("SK")) {
                test.type = table.sortkey_datatype;
                test.attribute = table.sort_key;
                test.values = query.SK.values;
                test.condition = query.SK.condition;
                pass = evaluate(item, test);
            }

            if (pass) {
                // test each filter condition
                $.each(query.filter, function (idx, filter) {
                    if (filter.operator == "OR")
                        if (pass)
                            // if pass is still true on an OR operator the test is done
                            return false;
                        else
                            // if pass is false on OR operator then set it to true and continue testing
                            pass = true;

                    if (pass)
                        pass = evaluate(item, filter);
                });
            }

            // add the item if it passed all condition checks
            if (pass)
                match_data.push(item);
        }
    });

    $("#queryDiv").hide();
    $("#runQueryDiv").hide();
    $(".remove").remove();
    $("#filterArea").hide();
    loadDataModel();
}

// evaluate whether an item passes a test or not
function evaluate(item, test) {
    var value = "",
        comparevalues = [];

    switch (test.type) {
        case "Boolean":
            value = getValue(item[test.attribute]) == true;
            $.each(test.values, function (idx, value) {
                test.values[idx].replace(value == "true");
            });
            break;

        case "N":
        case "Number":
            value = parseFloat(getValue(item[test.attribute]));
            $.each(test.values, function (idx, value) {
                test.values[idx].replace(parseFloat(value));
            });
            break;

        case "S":
        case "String":
            value = getValue(item[test.attribute]);
            break;
    }

    var testVal = false;
    switch (test.condition) {
        case ">":
            if (value > test.values[0])
                testVal = true;
            break;

        case ">=":
            if (value >= test.values[0])
                testVal = true;
            break;

        case "<":
            if (value < test.values[0])
                testVal = true;
            break;

        case "<=":
            if (value <= test.values[0])
                testVal = true;
            break;

        case "=":
            if (value == test.values[0])
                testVal = true;
            break;

        case "begins":
            if (value.startsWith(test.values[0]))
                testVal = true;
            break;

        case "between":
            var startVal = test.values[0],
                endVal = test.values[1];

            if (startVal > endVal) {
                startVal = endVal;
                endVal = test.values[0];
            }

            if (value > test.values[0] && value < test.values[1])
                testVal = true;
            break;

        case "contains":
            if (value.indexOf(test.values[0]) >= 0)
                testVal = true;
            break;

        case "in":
            $.each(test.values, function (idx, val) {
                if (value == val) {
                    testVal = true;
                    return false;
                }
            });
            break;
    }

    return testVal;
}