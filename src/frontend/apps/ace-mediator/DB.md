mapId: 5b96619b86f3cc8057216a03
rima.selected_UN_SDG

```sh
mongo
show dbs
use KnAllEdge
show collections
```

```sh
mongo
use KnAllEdge
```

https://docs.mongodb.com/v3.2/tutorial/query-documents/

Sorting
+ https://stackoverflow.com/questions/12517167/sorting-on-multiple-fields-mongo-db

Group
+ https://docs.mongodb.com/manual/reference/method/db.collection.group/
+ https://stackoverflow.com/questions/16662405/mongo-group-query-how-to-keep-fields

Aggregation
+ https://docs.mongodb.com/manual/reference/method/db.collection.aggregate/#db.collection.aggregate
+ https://docs.mongodb.com/manual/tutorial/aggregation-zip-code-data-set/
+ https://docs.mongodb.com/manual/reference/operator/aggregation/group/
+ examples
    + https://docs.mongodb.com/manual/tutorial/aggregation-zip-code-data-set/
    + https://stackoverflow.com/questions/6547441/mongodb-group-and-sort
+ sorting
    + https://docs.mongodb.com/manual/reference/operator/aggregation/sort/
    + https://docs.mongodb.com/manual/reference/operator/meta/orderby/


```js
// get all distinct emails
db.knodes.distinct( "dataContent.email" )

// not working
db.knodes.distinct( "dataContent.email", { mapId: "5b96619b86f3cc8057216a03" } )
// get all distinct emails in map
db.knodes.distinct( "dataContent.email", { mapId: ObjectId("5b96619b86f3cc8057216a03") } )


// get all distinct emails (and its count) in map
db.knodes.group({key: { 'dataContent.email': 1}, cond: { mapId: ObjectId("5b96619b86f3cc8057216a03") }, reduce: function ( curr, result ) { result.count ++ },initial: {count : 0 } })

// get number of occurences of each user (determined by email), its mapId and number of occurences
db.kedges.aggregate({
    $group: {
        _id: '$dataContent.email',
        mapId : { $first: '$mapId' },
        count: { $sum: 1 }
    }
})

// get all distinct sources (soirceId) of edges (and its count) in map
db.kedges.group({key: { 'sourceId': 1}, cond: { mapId: ObjectId("5b96619b86f3cc8057216a03") }, reduce: function ( curr, result ) { result.count ++ }, initial: {count : 0 } })

// find node with id
db.knodes.find({_id: ObjectId('5b4a16e800ea79029ca0c395')})


// get all distinct sources (soirceId) (and its count) of edges (of a type) in map
db.kedges.group({key: { 'sourceId': 1}, cond: {mapId: ObjectId("5b96619b86f3cc8057216a03"), type: 'rima.selected_UN_SDG'}, reduce: function ( curr, result ) { result.count ++ }, initial: {count : 0 } })

// get number of same emails
db.knodes.aggregate({
    $group: {
        _id: '$dataContent.email',
        mapId : { $first: '$mapId' },
        count: { $sum: 1 }
    }
})

// find all edges of a type
db.kedges.find({ type: 'rima.selected_UN_SDG' } )

// find all distinct sources of edges that are of a specific type
db.kedges.distinct( "sourceId", { type: 'rima.selected_UN_SDG' } )

// search for all users (`sourceId`) that have 'rima.selected_UN_SDG' edges in the map
// and count number of those edges for each user
db.kedges.aggregate(
    {$match:{
        mapId: ObjectId("5b96619b86f3cc8057216a03"),
        type: 'rima.selected_UN_SDG'
    }},
    {$group:{
        _id: "$sourceId",
        count: { $sum: 1 }
    }},
    {$sort:{
        count: -1,
        _id: 1
    }}
)

// search for all users (`iAmId`) in map that have dreams ('rima.user.dream') and
// shows number of dreams for each user ordered by number of dreams and then user
// and count number of those edges for each user
db.knodes.aggregate(
    {$match:{
        mapId: ObjectId("5b96619b86f3cc8057216a03"),
        type: 'rima.user.dream'
    }},
    {$group:{
        _id: "$iAmId",
        count: { $sum: 1 }
    }},
    {$sort:{
        count: -1,
        _id: 1
    }}
)

// search for all users (`iAmId`) in map that have dreams ('rima.user.dream') and
// shows number of dreams for each user ordered by number of dreams and then user
// and count number of those edges for each user
db.knodes.aggregate(
    {$match:{
        mapId: ObjectId("5b96619b86f3cc8057216a03"),
        type: 'rima.user'
    }},
    {$group:{
        _id: "$dataContent.email",
        iAmId : { $first: '$_id' },
        firstName : { $first: '$dataContent.firstName' },
        lastName : { $first: '$dataContent.lastName' },
        count: { $sum: 1 }
    }},
    {$sort:{
        count: -1
    }}
)

// get detail info for each user
db.knodes.find( { _id : { $in : [
    ObjectId("5b52221aa285f226fd381a82"), ObjectId("5b5221eef01f8b255c047ea3"),
    ObjectId("5b522209a285f226fd381a79"), ObjectId("5b5221e4f01f8b255c047e9d"),
    ObjectId("5b5221fdf01f8b255c047eb7")] } } );


{ "_id" : "sladjana.markovic08@gmail.com", "iAmId" : ObjectId("5b52221aa285f226fd381a82"), "firstName" : "Slađana", "lastName" : "Marković", "count" : 13 }
{ "_id" : "marko94@tippnet.rs", "iAmId" : ObjectId("5b5221eef01f8b255c047ea3"), "firstName" : "Marko", "lastName" : "Neskovic", "count" : 5 }
{ "_id" : "sabljic.99@gmail.com", "iAmId" : ObjectId("5b522209a285f226fd381a79"), "firstName" : "Milena", "lastName" : "Sabljic", "count" : 2 }
{ "_id" : "tina.sibinovic95@gmail.com", "iAmId" : ObjectId("5b5221e4f01f8b255c047e9d"), "firstName" : "Tijana", "lastName" : "Sibinovic", "count" : 2 }
{ "_id" : "mail.gavrilo@gmail.com", "iAmId" : ObjectId("5b5221fdf01f8b255c047eb7"), "firstName" : "Gavrilo", "lastName" : "Prodanović", "count" : 2 }
{ "_id" : "zmilica1997@gmail.com", "iAmId" : ObjectId("5b522217a285f226fd381a7f"), "firstName" : "Milica", "lastName" : "Zivanovic", "count" : 1 }
{ "_id" : "milan.ivkes97@gmail.com", "iAmId" : ObjectId("5b522203f01f8b255c047ec3"), "firstName" : "Milan", "lastName" : "Ivkovic", "count" : 1 }
{ "_id" : "suncicapopovic44@gmail.com", "iAmId" : ObjectId("5b522200f01f8b255c047ebc"), "firstName" : "Suncica", "lastName" : "Popovic", "count" : 1 }
{ "_id" : "katarinanikolic.96@gmail.com", "iAmId" : ObjectId("5b5221fef01f8b255c047eba"), "firstName" : "Katarina", "lastName" : "Nikolić", "count" : 1 }
{ "_id" : "m.aleksandra026@gmail.com", "iAmId" : ObjectId("5b5221fcf01f8b255c047eaf"), "firstName" : "Aleksandra ", "lastName" : "Mihajlović ", "count" : 1 }
{ "_id" : "nenadnikolickalis94@gmail.com", "iAmId" : ObjectId("5b5221f5f01f8b255c047eac"), "firstName" : "Nenad", "lastName" : "Nikolic", "count" : 1 }
{ "_id" : "baltybg89@gmail.com", "iAmId" : ObjectId("5b5221f2f01f8b255c047ea6"), "firstName" : "Aleksandar", "lastName" : "Pilipovic", "count" : 1 }
{ "_id" : "milicajagodina97@gmail.com", "iAmId" : ObjectId("5b5222ab692b782860fa6f94"), "firstName" : "Milica", "lastName" : "Ristic", "count" : 1 }
{ "_id" : "necke996-nis@hotmail.com", "iAmId" : ObjectId("5b522217a285f226fd381a7e"), "firstName" : "Nemanja", "lastName" : "Igić", "count" : 1 }
{ "_id" : "jankovic-tamara@hotmail.com", "iAmId" : ObjectId("5b5221f0f01f8b255c047ea4"), "firstName" : "Tamara", "lastName" : "Jankovic", "count" : 1 }
{ "_id" : "anja_erakovic@hotmail.com", "iAmId" : ObjectId("5b52216f84195625f3aabe45"), "firstName" : "Anja", "lastName" : "Erakovic", "count" : 1 }
{ "_id" : "doloresvrhovac@gmail.com", "iAmId" : ObjectId("5b52215c84195625f3aabe41"), "firstName" : "Dolores", "lastName" : "Vrhovac", "count" : 1 }
{ "_id" : "vukodlakljuti@gmail.com", "iAmId" : ObjectId("5b52216c84195625f3aabe43"), "firstName" : "Filip", "lastName" : "Ranković ", "count" : 1 }
{ "_id" : "miladinovick@yahoo.com", "iAmId" : ObjectId("5b5221ccf01f8b255c047e91"), "firstName" : "Katarina", "lastName" : "Miladinovic", "count" : 1 }
{ "_id" : "hooshyar.shariati@gmail.com", "iAmId" : ObjectId("5b5220fc84195625f3aabe3d"), "firstName" : "Hooshyar", "lastName" : "Shariati", "count" : 1 }
{ "_id" : "jovjovana998@gmail.com", "iAmId" : ObjectId("5b522215a285f226fd381a7c"), "firstName" : "Jovana", "lastName" : "Jovanoviv", "count" : 1 }
{ "_id" : "snwbrdabc@hotmail.com", "iAmId" : ObjectId("5b5221f2f01f8b255c047ea7"), "firstName" : "Ivan", "lastName" : "Nikolic", "count" : 1 }
{ "_id" : "jovansom95@gmail.com", "iAmId" : ObjectId("5b521ff984195625f3aabe35"), "firstName" : "Jovan", "lastName" : "Janicijevic", "count" : 1 }
{ "_id" : "ddenic888@gmail.com", "iAmId" : ObjectId("5b52215484195625f3aabe3f"), "firstName" : "Dragana", "lastName" : "Denic", "count" : 1 }
{ "_id" : "mirelagracanac269@gmail.com", "iAmId" : ObjectId("5b522187f01f8b255c047e87"), "firstName" : "Mirela", "lastName" : "Gračanac", "count" : 1 }
{ "_id" : "rikanovic19@gmail.com", "iAmId" : ObjectId("5b52202184195625f3aabe37"), "firstName" : "Savo", "lastName" : "Rikanović ", "count" : 1 }
{ "_id" : "marija.janicijevic.5.123@gmail.com", "iAmId" : ObjectId("5b52205084195625f3aabe39"), "firstName" : "Marija", "lastName" : "Janicijevic", "count" : 1 }
{ "_id" : "sivivuk2@gmail.com", "iAmId" : ObjectId("5b52205a84195625f3aabe3b"), "firstName" : "Vukman", "lastName" : "Božović", "count" : 1 }
{ "_id" : "akocic993@hotmail.rs", "iAmId" : ObjectId("5b5221f6f01f8b255c047eae"), "firstName" : "Aleksa", "lastName" : "Kocic", "count" : 1 }
{ "_id" : "aleksacakicktz@gmail.com", "iAmId" : ObjectId("5b5221dbf01f8b255c047e97"), "firstName" : "Aleksa", "lastName" : "Cakic", "count" : 1 }
{ "_id" : "milos.trijumf@gmail.com", "iAmId" : ObjectId("5b5221e1f01f8b255c047e9b"), "firstName" : "Milos", "lastName" : "Stosic", "count" : 1 }
{ "_id" : "radan.orasanin@hotmail.com", "iAmId" : ObjectId("5b5221c3f01f8b255c047e8d"), "firstName" : "Radan", "lastName" : "Orasanin", "count" : 1 }
{ "_id" : "vranic.rio@gmail.com", "iAmId" : ObjectId("5b522293692b782860fa6f92"), "firstName" : "Luka", "lastName" : "Vranic", "count" : 1 }
{ "_id" : "tasicandrijana23@gmail.com", "iAmId" : ObjectId("5b5221c7f01f8b255c047e8f"), "firstName" : "Andrijana ", "lastName" : "Tasic", "count" : 1 }
{ "_id" : "teastojkovic95@gmail.com", "iAmId" : ObjectId("5b522201f01f8b255c047ebd"), "firstName" : "Teodora", "lastName" : "Stojkovic", "count" : 1 }
{ "_id" : "nikolasijus@yahoo.com", "iAmId" : ObjectId("5b5221ddf01f8b255c047e99"), "firstName" : "Nikola", "lastName" : "Tonic", "count" : 1 }

{ "_id" : null, "iAmId" : ObjectId("5b522191f01f8b255c047e89"), "firstName" : null, "lastName" : null, "count" : 1 }

{ "_id" : "sinisa.rudan2@gmail.com", "iAmId" : ObjectId("5b522202f01f8b255c047ec0"), "firstName" : "Sinisa2", "lastName" : "Rudan", "count" : 1 }
{ "_id" : "sasa.rudan@gmail.com", "iAmId" : ObjectId("5b522228a285f226fd381a9b"), "firstName" : "Sasha", "lastName" : "Rudan", "count" : 1 }
{ "_id" : "mprinc@gmail.com", "iAmId" : ObjectId("5b522199f01f8b255c047e8b"), "firstName" : "Sasa", "lastName" : "Rudan", "count" : 1 }

type `it` to iterate

mongo
use KnAllEdge
