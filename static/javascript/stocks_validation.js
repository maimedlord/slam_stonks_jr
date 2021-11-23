{
  $jsonSchema: {
    bsonType: 'object',
    required: [
      '_id',
      'date',
      'name',
      'price',
      'short_interest',
      'float_shorted',
      'pytrend',
      'yf_hist_dataframe',
      'twitter_sentiment'
    ],
    properties: {
      _id: {
        bsonType: 'string',
        description: 'required: _id | ticker',
        minLength: 2,
        maxLength: 5
      },
      date: {
        bsonType: 'date',
        description: 'required: ISODate'
      },
      name: {
        bsonType: 'string',
        description: 'required: company name',
        minLength: 1,
        maxLength: 50
      },
      price: {
        bsonType: 'double',
        description: 'required: price',
        minimum: 0,
        maximum: 100000
      },
      short_interest: {
        bsonType: 'string',
        description: 'required: short_interest',
        minLength: 1,
        maxLength: 16
      },
      float_shorted: {
        bsonType: 'string',
        description: 'required: float_shorted',
        minLength: 1,
        maxLength: 7
      },
      pytrend: {
        bsonType: 'object',
        description: 'required: pytrend data'
      },
      yf_hist_dataframe: {
        bsonType: 'object',
        description: 'required: yfinance pandas DataFrame object'
      },
      twitter_sentiment: {
        bsonType: 'object',
        description: 'required: Twitter sentiment analysis',
        required: [
          'polarity',
          'subjectivity'
        ],
        properties: {
          polarity: {
            bsonType: 'array',
            description: 'required: polarity array'
          },
          subjectivity: {
            bsonType: 'array',
            description: 'required: subjectivity array'
          }
        }
      }
    }
  }
}