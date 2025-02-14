// UI logic and onclick handlers
$(document).ready(function() {
    var credStr = getCookie("credentials");
    
    if (credStr != "") {
        credentials = JSON.parse(credStr);
        initDynamoClient();
    }
    
    //file upload
    $("#importFile").change(function(e) {
        $("#fileDiv").hide();
        var reader = new FileReader();
        reader.onload = onReaderLoad;
        reader.readAsText(e.target.files[0]);
    });

    $(".btnImportOneTable").bind('click', function(evt) {
        importOneTableSchema($("#schema").text());
        $("#oneTableModal").hide();
    });

    $("#btnDefineMap").bind('click', function(evt) {
        if ($("#txtMapFunction").val().indexOf("${" + alertData.caller + "}") >= 0) {
            alert("Map Functions cannot reference the destination attribute.");
            return;
        }
        
        var valueTemplate = $("#txtMapFunction").val();
        debugger;
        makeChange();
        createMapping(alertData.data.type, alertData.caller, valueTemplate);
        loadDataModel();

        $("#txtMapFunction").val("");
        $("#lblEditMap").text("Mapping Function:");
        $("#selectTypeDiv").hide();
        $("#defineValueTemplateDiv").hide();
    });

    // generic click handler for Cancel buttons
    $('.cancel').bind('click', function(evt) {
        $("#createTableOrIndex").hide();
        $("#fileDiv").hide();
        $("#selectTableDiv").hide();
        $("#createModelDiv").hide();
        $("#alertModal").hide();
        $("#removeAttributeModal").hide();
        $("#oneTableModal").hide();
        $("#defineValueTemplateDiv").hide();
        $("#txtMapFunction").val("");
        $("#lblEditMap").text("Mapping Function:");
        $("#selectTypeDiv").hide();
        $("#txtMapFunction").prop("disabled", false);
        $("#btnDefineMap").prop("disabled", false);
        $("#schemaTableDiv").hide();
        $("#modelDiv").hide();

        initQuery();
    });

    // click handler for Create Model
    $("#btnCreateModel").click(function (evt) {
        // initialize the current model
        model = {};

        // populate metadata from the form and set created timestamp
        model.ModelName = $("#txtModelName").val();
        var date = new Date();
        model.ModelMetadata = {
            "Author": $("#txtModelAuthor").val(),
            "DateCreated": date,
            "DateLastModified": date,
            "Description": $("#txtModelDesc").val(),
            "AWSService": "Amazon DynamoDB",
            "Version": "2.0"
        };

        // initialize Model change buffer and add a new Table
        tableChanges = {};
        addTable();

        $("#createModelDiv").hide();
    });

    // hook the onchange event handler for the view table dropdown
    $("#viewTable").change(function (event) {
        $("#selectTableDiv").hide();

        if ($("#viewTable").val() == "-1") {
            // if create table was selected then fire add table dialog
            $("#selectTableDiv").hide();
            addTable();
        }
        else {
            // set the modelIndex to load
            modelIndex = parseInt($("#viewTable").val());

            // initialize tab index and load the selected data model
            loadDataModel();
        }

        findDataModels();

    });

    $("#createTableOrIndex").find(".input_key_select").on('change', function() {
        var sel = $(this).val();
        if (sel == "include") {
            $(".inputkey_group").show();
            gsi_attrkey = "include";
        } else {
            $(".inputkey_group").hide();
            gsi_attrkey = "all";
        }
        gsi_attrlist = [];
    });

    // click handler for Create Table
    $("#createTableOrIndex").find(".btn_tablecreate").on('click', function() {
        var definition = {},
            isTable = $("#title h1").text() == "Create Table";

        if ($('.gsi_primary').val() == '') {
            alert("Please provide a patition key!");
            return;
        }

        if ($('.cgi_title').val() == '') {
            alert("Please provide a name");
            return;
        }

        definition.KeyAttributes = {};
        let indexName = $('.cgi_title').val();
        definition[isTable ? "TableName" : "IndexName"] = indexName
        definition.KeyAttributes.PartitionKey = {
            "AttributeName": $('.gsi_primary').val(),
            "AttributeType": $('#dropPart').val()
        };
        definition.KeyAttributes.SortKey =  {
            "AttributeName": $('.gsi_sort').val(),
            "AttributeType": $('#dropSort').val()
        };

        if (!isTable) {
            definition["Projection"] = {
                "ProjectionType": "ALL"
            };

            makeChange();
            datamodel.GlobalSecondaryIndexes.push(definition);
            schema.indexes[indexName] = {
                hash: $('.gsi_primary').val(),
                sort: $('.gsi_sort').val(),
                projection: 'ALL',
            }
        } else {
            datamodel = {
                "TableName": definition.TableName,
                "KeyAttributes": definition.KeyAttributes,
                "NonKeyAttributes":[],
                "GlobalSecondaryIndexes": [],
                "TableData": []
            };

            if (model.DataModel == null)
                model.DataModel = []

            model.DataModel.push(datamodel);
            modelIndex = model.DataModel.length - 1;

            json_data = datamodel.TableData;

            table.name = definition.TableName;
            table.partition_key = $('.gsi_primary').val();
            table.sort_key = $('.gsi_sort').val();
            table.sortkey_datatype = $('.dropSort').val();
            tableChanges[datamodel.TableName] = [];

            schema.indexes.primary = {
                hash: $('.gsi_primary').val(),
                sort: $('.gsi_sort').val(),
            }
            addItem("~new~");
        }
        $("#createTableOrIndex").find('.key_input').val('');
        $('#createTableOrIndex').toggle();

        findDataModels();
        loadDataModel();
    });

    $("#createTableOrIndex").find(".btn_attrkey").on("click", function() {
        gsi_attrkey = $("#createTableOrIndex").find(".input_key_select").val();
        var html = '';
        var atrkey = $("#createTableOrIndex").find(".attrkey_input").val();
        if (atrkey.trim() == '') {
            alert("Please input key");
            return;
        }
        if (gsi_attrkey == 'include') {
            html = '<li>' + atrkey + '</li>';
            gsi_attrlist.push(atrkey);
        } else {

        }
    });

    $("#loadModel").on('click', function() {
        $("#mySidenav").css("width","0");
        $("#saveCredsDiv").hide();
        $("#fileDiv").show();
        
        $("#fileType").text("Load Model");
        $("#loadType").text("Select a model:");
        
        alertData.caller = "loadModel";
    });
    
    $("#loadCreds").on('click', function() {
        $("#mySidenav").css("width","0");
        $("#saveCredsDiv").prop('checked', false);
        $("#saveCredsDiv").show();
        $("#fileDiv").show();
        
        $("#fileType").text("Load Credentials");
        $("#loadType").text("Select credentials file:");
        
        alertData.caller = "loadCreds";
    });
    
    $("#saveToTable").on('click', function() {
        alertData.caller = "save";
        $("#lblLoadSave").text("Save to Table");
        $("#mySidenav").css("width","0");
        $("#schemaTableDiv").show();
    });
    
    $("#loadFromTable").on('click', function() {
        alertData.caller = "load";
        $("#selectModel").val("none");
        $("#lblLoadSave").text("Load from Table");
        $("#mySidenav").css("width","0");
        $("#schemaTableDiv").show();
    });

    $(".addGSI").on('click', function() {
        $("#mySidenav").css("width","0");
        $("#title h1").text("Create Index");
        $("#idx_lbl").text("Index name:");
        $("#tbSort").show();
        $("#dropSort").show();
        $("#projection_cfg").show();
        $('#createTableOrIndex').toggle();
    });

    $("#createModel").on('click', function() {
        $("#mySidenav").css("width","0");
        if (model.ModelName != null) {
            alertData = {
                caller: "createModel",
                data: ""
            };

            $("#alertTitle h1").text("Model Overwrite");
            $("#alertText").text("The existing model will be overwritten, continue?");

            $("#alertModal").show();
        }
        else
            $("#createModelDiv").show();
    });

    $("#saveModel").on('click', function() {
        $("#mySidenav").css("width","0");
        saveModel();
    });

    $("#clearIdx").on('click', function() {
        $("#mySidenav").css("width","0");
        datamodel.GlobalSecondaryIndexes = [];
        loadDataModel();
    });

    $("#importSchema").on('click', function() {
        $("#oneTableModal").show();
    });

    $("#showValues").on('click', function(e) {
        showValues = !showValues
        showTable();
        $("#showValuesCheckbox").prop("checked", showValues);
        e.preventDefault()
    });

    $("#showValuesCheckbox").prop("checked", true);

    $("#exportSchema").on('click', function() {
        $("#mySidenav").css("width","0");
        exportOneTableSchema();
    });

    $("#reload").on('click', function() {
        location.reload();
    });
});