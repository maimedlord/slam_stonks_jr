{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      'date',
      'top10array'
    ],
    properties: {
      date: {
        bsonType: 'date',
        description: 'required: ISODate'
      },
      top10array: {
        bsonType: 'array',
        description: 'required: array of strings (tickers) // min&max=10',
        minItems: 10,
        maxItems: 10
      }
    }
  }
}