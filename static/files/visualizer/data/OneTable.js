{
    indexes: {
        primary: {
            hash: 'PK',
            sort: 'SK'
        },
        gsi1: {
            hash: 'PK1',
            sort: 'SK1',
            projection: 'ALL'
        },
        gsi2: {
            hash: 'PK2',
            sort: 'SK2',
            projection: 'ALL'
        },
        gsi3: {
            hash: 'PK3',
            sort: 'SK3',
            projection: 'ALL'
        },
        gsi4: {
            hash: 'PK4',
            sort: 'SK4',
            projection: 'ALL'
        }
    },
    models: {
        activity: {
            PK:             { type: String, value: 'activity#${date}' },
            SK:             { type: String, value: 'activity#' },
            PK1:            { type: String },
            SK1:            { type: String },
            timestamp:      { type: Date, required: true },
            description:    { type: String },
        },
        admission: {
            PK:             { type: String, value: 'admission#${patientId}' },
            SK:             { type: String, value: 'admission#${timestamp}#{roomId}' },
            timestamp:      { type: Date },
            roomId:         { type: String },
            condition:      { type: String },
            patientId:      { type: String },
            PK1:            { type: String },
            SK1:            { type: String },
            PK2:            { type: String },
            SK2:            { type: String }
        },
        doctor: {
            PK:             { type: String, value: 'doctor#${name}' },
            SK:             { type: String, value: 'doctor#' },
            name:           { type: String, required: true },
            PK1:            { type: String },
            SK1:            { type: String },
            PK2:            { type: String },
            SK2:            { type: String }
        },
        medicine: {
            PK:             { type: String, value: 'medicine#${name}' },
            SK:             { type: String, value: 'medicine#' },
            name:           { type: String },
            PK1:            { type: String },
            SK1:            { type: String },
            PK2:            { type: String },
            SK2:            { type: String }
        },
        nurse: {
            PK:             { type: String, value: 'nurse#${name}' },
            SK:             { type: String, value: 'nurse#' },
            name:           { type: String, required: true },
            PK1:            { type: String },
            SK1:            { type: String },
        },
        patient: {
            PK:             { type: String, value: 'patient#${name}' },
            SK:             { type: String, value: 'patient#' },
            name:           { type: String, required: true },
            age:            { type: Number, required: true },
            medicare:       { type: String },
        },
        room: {
            PK:             { type: String, value: 'room#${roomId}' },
            SK:             { type: String, value: 'room#' },
            PK3:            { type: String },
            SK3:            { type: String },
            roomId:         { type: String, required: true },
            building:       { type: String, required: true },
        },
        treatment: {
            PK:             { type: String, value: 'treatment#${treatmentId}' },
            SK:             { type: String, value: 'treatment#${timestamp}#${treatmentId}' },
            timestamp:      { type: Date },
            treatmentId:    { type: String },
            description:    { type: String },
            PK1:            { type: String },
            SK1:            { type: String },
            PK2:            { type: String },
            SK2:            { type: String }
        },
    },
    data: [
        {
            PK: "P1",
            SK: "A",
            type: "patient",
            name: "John Morrison",
        },
        {
            PK: "P1",
            SK: "2020-11-25T12:00:00#T1",
            type: "treatment",
            timestamp: "2020-11-25T12:00:00",
            treatmentId: "T11",
            description: "Covid-19 vaccination",
            PK1: "D1",
            SK: "2020-11-25T12:00:00",
            PK2: "hospitalId-T",
            SK2: "2020-11-25T12:00:00"
        },
        {
            PK: "P1",
            SK: "2020-11-25T12:00:00#M1",
            type: "medicine",
            name: "Pfizer Covid-19",
            PK1: "D1",
            SK: "2020-11-25T12:00:00",
            PK2: "hospitalId-M",
            SK2: "2020-11-25T12:00:00"
        },
        {
            PK: "P1",
            SK: "2020-11-25T12:00:00#R1",
            type: "admission",
            timestamp: "2020-11-25T12:00:00",
            roomId: "R1",
            PK1: "N1",
            SK: "2020-11-25T12:00:00",
            PK2: "normal",
            SK2: "2020-11-26T00:00:00",
            PK3: "R1",
            SK3: "2020-11-25T12:00:00",
            PK4: "hospitalId",
            SK4: "2020-11-25T12:00:00",
            "condition": "Covid-19 test"
        },
        {
            PK: "D1",
            SK: "A",
            type: "doctor",
            name: "Dr. Z. Smith",
            PK1: "D1",
            SK: "A",
            PK2: "specialty",
            SK2: "hospitalId"
        },
        {
            PK: "N1",
            SK: "A",
            type: "nurse",
            name: "Ms. E. Jones",
            PK1: "N1",
            SK: "A"
        },
        {
            PK: "R1",
            SK: "A",
            type: "room",
            roomId: "R1",
            building: "East Wing",
            PK3: "R1",
            SK3: "A"
        },
        {
            PK: "P1",
            SK: "2020-11-25T12:00:00#A1",
            type: "activity",
            PK1: "N1",
            SK: "2020-11-25T12:00:00"
        }
    ]
}
