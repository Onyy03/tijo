export const MERCHANT_NAME = 'Delikatesy Kłos'

export const MAX_QUANTITY = 9

// prices in grosze, like amounts in the backend
export const PRODUCTS = [
  {
    id: 'bread',
    name: 'Chleb żytni na zakwasie',
    details: '700 g · wypiekany o 5:00',
    priceCents: 1290,
    swatch: '#b9773d',
  },
  {
    id: 'coffee',
    name: 'Kawa ziarnista Brazylia Santos',
    details: '250 g · średnio palona',
    priceCents: 3490,
    swatch: '#4e3322',
  },
  {
    id: 'butter',
    name: 'Masło ekstra 82%',
    details: '200 g',
    priceCents: 899,
    swatch: '#d9b94f',
  },
  {
    id: 'honey',
    name: 'Miód gryczany',
    details: '400 g · z pasieki rodzinnej',
    priceCents: 2650,
    swatch: '#8f4a22',
  },
  {
    id: 'olive-oil',
    name: 'Oliwa z oliwek extra virgin',
    details: '500 ml · tłoczona na zimno',
    priceCents: 3999,
    swatch: '#6f7a32',
  },
  {
    id: 'espresso-machine',
    name: 'Ekspres kolbowy Barista Pro',
    details: 'stal nierdzewna · 15 barów',
    priceCents: 129900,
    swatch: '#3d4246',
  },
]

export const INITIAL_CART = { bread: 1, coffee: 1 }
