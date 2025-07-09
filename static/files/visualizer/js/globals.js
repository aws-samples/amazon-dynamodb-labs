var // container for the data model
    model = {},
    // pointer to model.DataModel[modelIndex]
    datamodel = {},
    // pointer to model.DataModels[0].TableData
    json_data = [],
    // container for change history (up to 50 revisions per table in the model)
    tableChanges = {},
    // container for the current table
    // properties: name, partition_key, sort_key, sortkey_datatype
    table = {},
    // holders for the current keys and data types used by makeTable()/makeIndex()/generate()
    partition_key,
    sort_key,
    sortkey_datatype,
    // list of unique values by attribute name
    unique_values = {},
    // gsi projection settings for new GSI
    gsi_attrkey = 'all',
    gsi_attrlist = [],
    // list of values from attributes with Map type
    vals = [],
    // Attribute element counter
    tabIndex = 0,
    // the object to focus when table is rendered
    selectId = {},
    // keypress event flag;
    fired = true,
    // current DataModel index
    modelIndex = 0,
    // container for alert data
    alertData = {
        caller: "",
        data: ""
    },
    // onClick event indicator to avoid double firing updates
    mouseDown = false,
    // container to hold first and last Attribute cells
    boundary = {
        first: {},
        last: {}
    },
    // container for Attribute cell metadata
    cellId = {},
    // the Item clipboard
    pasteItem = {},
    // number of filters for the currently loaded query
    numFilters = 0,
    // collection of items matching the current query
    match_data = [],    
    // Show values vs types/templates
    showValues = true,
    // AWS account credentials
    credentials,
    client,
    dynamodb,
    accountTables,
    saveTable;

const DefaultSchema = {
    indexes: {},
    models: {},
    queries: {},
    data: [],
}

const types = {
    "String": "S", 
    "Number": "N", 
    "Binary": "B",
    "Boolean": "BOOL", 
    "Null": "NULL",
    "Map": "M",
    "List": "L",
    "StringSet": "SS",
    "NumberSet": "NS",
    "BinarySet": "BS"
}

/*
    Schema defining indexes, entity models.
*/
var schema = {
    indexes: { /*
        primary: { hash: 'partition-key-name', sort: 'sort-key-name' }
        gs1: { hash: 'partition-key-name', sort: 'sort-key-name' }
    */ },
    models: { /*
        map             String. Either simple attribute name or "attribute.property".
        default         String. Default value string or function.
        foreign         String. Reference to another entity model (model:keys)
        nulls           Boolean. Allow property to be set to null.
        required        Boolean. Attribute is always required.
        size            Number. Maximum size of the data value
        type            String: String, Boolean, Number, Date, Set, Buffer, Binary, Set, Object, Array
        validate        String. Regular expression to match data (/regexp/qualifiers)
        value           String|Function. Value string template, function (mapping function)
        unique          Boolean. Attribute must have a unique value

        //  Not proposed to implement
        crypt           Boolean
        enum            Array of values
        filter          Boolean. Prevent a property from being used in a filter
        hidden          Boolean Don't return the attributes to API callers.
        transform       Transform hook function
        uuid            ‘uuid | ulid | ksuid'
    */ },

    //  Present on import / export
    queries: {},
    data: {},
}