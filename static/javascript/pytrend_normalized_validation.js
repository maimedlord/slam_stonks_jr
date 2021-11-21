{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      'date',
      'pytrend_normalized'
    ],
    properties: {
      date: {
        bsonType: 'date',
        description: 'required: ISODate'
      },
      pytrend_normalized: {
        bsonType: 'object',
        description: 'required: object containing pytrend_normalized data objects'
      }
    }
  }
}