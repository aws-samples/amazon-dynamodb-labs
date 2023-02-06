# --------------------------------------------------------------------------------------------------
# AWS Settings
# --------------------------------------------------------------------------------------------------

# Kinesis
KINESIS_STREAM_NAME             = 'IncomingDataStream'

# DynamoDB Table and Column Names
STATE_TABLE_NAME                = 'StateTable'
STATE_TABLE_KEY                 = 'id'

DELTA_TABLE_NAME                = 'ReduceTable'
DELTA_TABLE_KEY                 = 'MessageId'

AGGREGATE_TABLE_NAME            = 'AggregateTable'
AGGREGATE_TABLE_KEY             = 'Identifier'

MESSAGE_COUNT_NAME              = 'message_count'

PARAMETER_TABLE_NAME            = 'ParameterTable'
PARAMETER_TABLE_KEY             = 'parameter'
PARAMETER_COLUMN_NAME           = 'value'

ID_COLUMN_NAME                  = 'TradeID'
VERSION_COLUMN_NAME             = 'Version'
VALUE_COLUMN_NAME               = 'Value'
TIMESTAMP_COLUMN_NAME           = 'Timestamp'
HIERARCHY_COLUMN_NAME           = 'Hierarchy'

HIERARCHY_DEFINITION            =  {
                                    'RiskType'  : ['PV', 'Delta'],
                                    'Region'    : ['EMEA', 'APAC', 'AMER'],
                                    'TradeDesk' : ['FXSpot', 'FXOptions']
                                }

TIMESTAMP_GENERATOR_FIRST       = 'timestamp_generator_first'
TIMESTAMP_GENERATOR_MEAN        = 'timestamp_generator_mean'
   
# --------------------------------------------------------------------------------------------------
# Aggregation Settings
# --------------------------------------------------------------------------------------------------

# Definition of the Hierarchy
AGGREGATION_HIERARCHY = ['RiskType', 'TradeDesk', 'Region']