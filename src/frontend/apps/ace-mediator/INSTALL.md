# Performing Sustainable CoEvolution (PSC)

# INSTALL

***NOTE***: Before installing this app you need to install **Colabo.Space** ***tools***, ***backend*** and ***fronted***. Please read how to install them in the [INSTALL.md](../../../INSTALL.md) document.

```sh
cd src/frontend/apps/psc #the folder where this INSTALL.MD documnet is residing too
yarn
```

## Install Frontend Colabo Puzzles (Packages)

***NOTE***: This is done automatically during the install process (please check the script `prepare` inside the `package.json`) and it is not necessary to be done manually.

# Run

```sh
cd src/frontend/apps/psc
# run predefined npm script
npm start
# run with local ng
./node_modules/\@angular/cli/bin/ng serve -o -p 8891
# run with local ng using npx
npx ng serve -o --port 8891
# or with global ng
ng serve -o -p 8891
# or with default port (`angular.json` (architect.serve.options.port)) and without openning browser (no `-o`)
ng serve
```

# Deploy

https://fv.colabo.space/ redirects to **/var/www/fv**

## Build

This procedure is only if we don't use **Ansimble** as automated solution.

This part is done on the local dev machine:

```sh
cd src/frontend/apps/psc
ng build --prod --build-optimizer

# run on local server (JUST for testing, not necessary)
# then open url: localhost:8000
cd dist/performing_sustainable_coevolution
python -m SimpleHTTPServer 8000
```

## Code/Data Upload

Uploading the build code on the server (right now the: ***158.39.75.120***)

```sh
#the code is built in the following folder:
cd src/frontend/apps/psc/dist/performing_sustainable_coevolution/
#we put the content of this folder into the server folder:
/var/www/fv
# ⚠️ !⚠️ !⚠️ we copy all but the 'config' folder (we do DO NOT OVERWRITE the 'config') !⚠️ !⚠️
#
# 
# if we have to change server the CONFIG FILE 
# then we copy the file
# 'colabo.space-infrastructure/provisioning/files/frontend/global-server.js'
# to /var/www/fv/config/global.js
# (by also renaming it from 'global-server.js' to 'global.js')
# !⚠️!⚠️ in the file we have to set the RESTfull backend API url in the file
# from
# serverUrl: 'http://127.0.0.1:8001', //local
# to
# serverUrl: 'https://fv.colabo.space/api', // colabo-space-1 (https)
```

# KnAllEdge content

!!!:warning: !⚠️ !⚠️ !⚠️ the **actual content** is migrated to

`src/frontend/apps/psc/docs/dbSetUp-CivilCourage.json`

!⚠️ !⚠️ !⚠️ !⚠️ !⚠️ 

## Map

Add map in kmaps (`right button > insert document`):

```json
{
    "_id" : ObjectId("5b96619b86f3cc8057216a03"),
    "name" : "Performing Sustainable CoEvolution @ PTW2018",
    "rootNodeId" : ObjectId("5b9662cb86f3cc8057216a09"),
    "type" : "CoLaboArthon",
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "parentMapId" : "",
    "dataContent" : null,
    "updatedAt" : ISODate("2018-09-10T01:07:10.401+0000"),
    "createdAt" : ISODate("2018-09-10T01:07:10.400+0000"),
    "isPublic" : true,
    "participants" : [
        ObjectId("556760847125996dc1a4a24f")
    ],
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
}
```

## ROOT node

Add ROOT node in knodes (`right button > insert document`):

```json
{
    "_id" : ObjectId("5b9662cb86f3cc8057216a09"),
    "name" : "Performing Sustainable CoEvolution @ PTW2018",
    "type" : "model_component",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:07:10.401+0000"),
    "createdAt" : ISODate("2018-09-10T01:07:10.400+0000"),
    "visual" : {
        "isOpen" : true,
        "yM" : NumberInt(0),
        "xM" : NumberInt(0)
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0),
    "decorations" : {

    },
    "up" : {

    },
    "dataContent" : {
        "propertyType" : "text/markdown",
        "property" : "Welcome to 'Performing Sustainable CoEvolution @ PTW2018'"
    }
}
```

## USERS

Add USERS node in knodes (`right button > insert document`):

```json
{
    "_id" : ObjectId("5b96691086f3cc8057216a13"),
    "name" : "Users",
    "type" : "rima.users",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0),
    "decorations" : {

    },
    "up" : {

    },
    "dataContent" : {
    }
}
```

edge:

```json
{
    "_id" : ObjectId("5b96698e86f3cc8057216a14"),
    "name" : "Users",
    "type" : "rima.users",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b49e94636390f03580ac9a8"),
    "targetId" : ObjectId("5b96691086f3cc8057216a13"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:18:20.619+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.618+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
}
```

## ColaboFlow

```json
{
    "_id" : ObjectId("5b9f9ff97f07953d41256aff"),
    "name" : "DIALO_GAME_STATE",
    "type" : "colaboflow.state",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
    "visual" : {
        "isOpen" : false
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0),
    "decorations" : {

    },
    "up" : {

    },
    "dataContent" : {
        "state": 0,
        "playRound": 1
    }
}
```

## CONTENT

Add CONTENT node in knodes (`right button > insert document`):

```json
{
    "_id" : ObjectId("5b966a1286f3cc8057216a17"),
    "name" : "Content",
    "type" : "clathon.content",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "visual" : {
        "isOpen" : true
    },
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0),
    "decorations" : {

    },
    "up" : {

    },
    "dataContent" : {

    }
}
```

Add CONTENT edge in kedges (`right button > insert document`):

```json
{
    "_id" : ObjectId("5b966a3386f3cc8057216a18"),
    "name" : "Content",
    "type" : "clathon.content",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b49e94636390f03580ac9a8"),
    "targetId" : ObjectId("5b966a1286f3cc8057216a17"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
}
```

## SDGs

Add SDG node in knodes (`right button > insert document`):

```json
{
    "_id" : ObjectId("5b9669e986f3cc8057216a15"),
    "name" : "SDGs",
    "type" : "const.sdgs",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:25:34.694+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.693+0000"),
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0),
    "decorations" : {

    },
    "up" : {

    },
    "dataContent" : {
    }
}
```

Add SDG edge in kedges (`right button > insert document`):

```json
{
    "_id" : ObjectId("5b966a0086f3cc8057216a16"),
    "name" : "SDGs",
    "type" : "const.sdgs",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b4a91d800ea790a4738a6e5"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b49e94636390f03580ac9a8"),
    "targetId" : ObjectId("5af39f8e2843ddf04b459cba"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
}
```

## SDGs Population

**Nodes:**

Add SDG nodes in `knodes`  (`right button > Paste document(s)...`):

I18N support according to the approach:

- https://medium.com/@_PierreMary/approache-to-mongodb-internationalisation-i18n-with-meteor-584933ae71dc
- https://github.com/TAPevents/tap-i18n-db

```JSON
[
  {
      "name" : "NO POVERTY",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(1),
          goal: "To end poverty in all its forms everywhere by 2030.",
          desc: "More than 700 million people still live in extreme poverty and are struggling to fulfil the most basic needs like health, education, and access to water and sanitation, to name a few.The overwhelming majority of people living on less than $1.90 a day live in Southern Asia and sub-Saharan Africa. However, this issue also affects developed countries. Right now there are 30 million children growing up poor in the world’s richest countries",

      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "БЕЗ СИРОМАШТВА",
            dataContent: {
          		goal:  "Превазићи сиромаштво у свим облицима свуда у свету до 2030. године.",
            	desc: "Више од 700 милиона људи још увек живе у условима екстремног сиромаштва и боре се да задовоље своје најосновније животне потребе као што су здравље, образовање, приступ води и санитарним условима итд. Огромна већина људи који преживљавају са мање од  1.90 долара дневно живе у јужној Азији и потсахарској Африци. Међутим, овај проблем такође погађа и развијене земље. Тренутно има преко 30 милиона деце која живе у сиромаштву у најбогатијим земљама света."
            }   
		}   
      }
  },
  {
      "name" : "ZERO HUNGER",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(2),
          goal:  "To end hunger, achieve food security and improved nutrition and promote sustainable agriculture",
          desc: "A profound change of the global food and agriculture system is needed to nourish today’s 795 million hungry and the additional 2 billion people expected by 2050. Extreme hunger and malnutrition remains a barrier to sustainable development and creates a trap from which people cannot easily escape. Hunger and malnutrition mean less productive individuals, who are more prone to disease and thus often unable to earn more and improve their livelihoods."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "БЕЗ ГЛАДИ",
            dataContent: {
          		goal:  "Сузбити глад, обезбедити сигуран приступ храни, квалитетнију исхрану и промовисати одрживу пољопривреду",
            	desc: "Неопходна је темељна промена у глобалним системима земљорадње и обезбеђивања хране како би се прехранило данашњих 795 милиона гладних и додатних 2 милијарде људи који ће се према очекивањима придружити овом броју до 2050. године.  Екстремна глад и потхрањеност су и даље препрека одрживом развоју и представљају замку из које се људи не могу лако ослободити. Глад и потхрањеност значе мањи број продуктивних појединаца који су истовремено склонији болестима и самим тим онемогућени да зараде више и поправе своје животне услове."
            }   
		}   
      }
  },
  {
      "name" : "GOOD HEALTH AND WELL-BEING FOR PEOPLE",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(3),
          goal:  "Ensure healthy lives and promote well-being for all at all ages",
          desc: "Мore than 6 million children still die before their fifth birthday every year. 16,000 children die each day from preventable diseases such as measles and tuberculosis. Every day hundreds of women die during pregnancy or from child-birth related complications. In many rural areas, only 56 percent of births are attended by skilled professionals. AIDS is now the leading cause of death among teenagers in sub-Saharan Africa, a region still severely devastated by the HIV epidemic"
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ДОБРО ЗДРАВЉЕ И БЛАГОСТАЊЕ",
            dataContent: {
          		goal:  "Обезбедити здрав живот и промовисати благостање за све грађане у свим животним добима",
            	desc: "Више од 6 милиона деце још увек умре пре свог петог рођендана сваке године. Шеснаест хиљада деце сваке године умре од болести које се могу спречити као што су заушке или туберкулоза. Сваког дана стотине жена умру током трудноће или од пост-порођајних компликација. У многим руралним областима, свега 56% порођаја обави адекватно обучено стручно особље. Сида је сада водећи узрок смртности међу тинејџерима у потсахарској Африци, која још увек представља област опустошену епидемијом вируса ХИВ-а"
            }   
		}   
      }
  },
  {
      "name" : "QUALITY EDUCATION",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(4),
          goal:  "Ensure inclusive and quality education for all and promote lifelong learning",
          desc: "While Sub-Saharan Africa made the greatest progress in primary school enrolment among all developing regions – from 52 percent in 1990, up to 78 percent in 2012 – large disparities still remain. Children from the poorest households are up to four times more likely to be out of school than those of the richest households. Disparities between rural and urban areas also remain high."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	"name" : "КВАЛИТЕТНО ОБРАЗОВАЊЕ",
            dataContent: {
          		goal:  "Обезбедити инклузивно и квалитетно образовање за све и промовисати учење током целог живота",
          		desc: "Упркос томе што је потсахарска Африка постигла највећи напредак у погледу броја уписаних ђака у основне школе међу свим регионима у развоју - са 52 процента у 1990. години до 78 процената у 2012. години - и даље остају велике недоследности. Постоји до четири пута већа вероватноћа да деца из најсиромашнијих домаћинстава нису укључена у образовни систем у односу на децу из најбогатијих домаћинства. Недоследност између руралних и урбаних подручја је такође и даље велика."
            }   
		}   
      }
  },
  {
      "name" : "GENDER EQUALITY",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(5),
          goal:  "Achieve gender equality and empower all women and girls",
          desc: "There are still huge inequalities in the labour market in some regions, with women systematically denied equal access to jobs. Sexual violence and exploitation, the unequal division of unpaid care and domestic work, and discrimination in public office, all remain huge barriers. It has been proven time and again, that empowering women and girls has a multiplier effect, and helps drive up economic growth and development across the board."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	"name" : "ЈЕДНАКОСТ ПОЛОВА",
            dataContent: {
          		goal:  "Остварити једнакост полова и оснажити све жене и девојке",
         		desc: "Још увек постоји велики проблем неједнакости на тржишту рада у неким регионима, док се женама систематски ускраћује једнак приступ пословима. Сексуално насиље и експлоатација, неједнака заступљеност полова у неплаћеним пословима бриге и неге, рад у домаћинству и дискриминација на јавним функцијама остају огромне препреке. Увек се изнова доказује да оснаживање жена и девојака има вишеструки ефекат и помаже да се успостави економски раст и развој у свим областима."
            }   
		}   
      }
  },
  {
      "name" : "CLEAN WATER AND SANITATION",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(6),
          goal:  "Ensure access to water and sanitation for all",
          desc: "Water scarcity affects more than 40 percent of people around the world, an alarming figure that is projected to increase with the rise of global temperatures as a result of climate change. In 2011, 10 countries are close to depleting their supply of renewable freshwater and must now rely on alternative sources. By 2050, it is projected that at least one in four people will be affected by recurring water shortages."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	"name" : "ЧИСТА ВОДА И САНИТАРИЈЕ",
            dataContent: {
          		goal:  "Обезбедити приступ води и санитарним условима за све",
          		desc: "Оскудица воде погађа више од 40%  људи широм света, што представља узнемирујући податак а тај број ће према проценама расти с порастом глобалних температура које су последица климатских промена. Према подацима из 2011. године, 10 земаља су биле близу исцрпљивања обновљивих ресурса воде за пиће и сада морају да се ослањају на алтернативне изворе. Процењује се да ће до 2050. године бар један од четворо људи бити погођен несташицом воде."
            }   
		}   
      }
  },
  {
      "name" : "AFORDABLE AND CLEAN ENERGY",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(7),
          goal:  "Ensure access to affordable, reliable, sustainable and modern energy for all",
          desc: " Between 1990 and 2010, the number of people with access to electricity has increased by 1.7 billion, and as the global population continues to rise so will the demand for cheap energy. A global economy reliant on fossil fuels, and the increase of greenhouse gas emissions is creating drastic changes to our climate system. This is impacting every continent. One in five people lack access to electricity, and as the demand continues to rise there needs to be a substantial increase in the production of renewable energy across the world."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ДОСТУПНА И ЧИСТА ЕНЕРГИЈА",
            dataContent: {
          		goal:  "Обезбедити приступ приступачним, поузданим, одрживим и савременим изворима енергије за све грађане",
            	desc: "Између 1990. и 2010. године, број људи с приступом електричној енергији порастао је за 1,7 милијарди, а како се глобално становништво и даље повећава, повећаваће се и потреба за јефтином енергијом. Глобална економија која се ослања на потрошљу фосилних горива, као и повећање емисије гасова с ефектом стаклене баште ствара драстичне промене у нашем климатском систему, што  утиче на сваки континент. Једна од пет особа нема приступ електричној енергији, а како потражња наставља да расте, неопходно је значајно повећање производње обновљиве енергије широм света."
            }   
		}   
      }
  },
  {
      "name" : "DECENT WORK AND ECONOMIC GROWTH",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(8),
          goal:  "Promote inclusive and sustainable economic growth, employment and decent work for all",
          desc: "In developing countries, the middle class now makes up more than 34 percent of total employment – a number that has almost tripled between 1991 and 2015 However, as the global economy continues to recover we are seeing slower growth, widening inequalities, and not enough jobs to keep up with a growing labour force. According to the International Labour Organization, more than 204 million people were unemployed in 2015."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ДОСТОЈАН РАД И ЕКОНОМСКИ РАСТ",
            dataContent: {
          		goal:  "Промовисати инклузиван и одржив економски раст, запосленост и хумане радне услове за све",
            	desc: "У земљама у развоју средња класа сада чини више од 34% укупног броја запослених, што представља скоро утростручен број људи у периоду између 1991. и 2015. године. Међутим, у потоњим фазама опоравка глобалне  економије, темпо раста се успорава док се продубљују неједнакости а број радних места је недовољан да би оджао корак с растућом радном снагом. На основу података Међународне организације рада, више од 204 милиона људи било је незапослено у 2015. години"
            }   
		}   
      }
  },
  {
      "name" : "INDUSTRY, INNOVATION AND INFRASTRUCTURE",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(9),
          goal:  "Build resilient infrastructure, promote sustainable industrialization and foster innovation",
          desc: "With over half the world population now living in cities, mass transport and renewable energy are becoming ever more important, as are the growth of new industries and information and communication technologies. Promoting sustainable industries, and investing in scientific research and innovation, are all important ways to facilitate sustainable development. More than 4 billion people still do not have access to the Internet, and 90 percent are from the developing world."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ИНДУСТРИЈА, ИНОВАЦИЈА И ИНФРАСТРУКТУРА",
            dataContent: {
          		goal:  "Изградити стабилну инфраструктуру, промивисати одрживу индустријализацију и неговати иновативност",
            	desc: "С обзиром да више од половине светске популације сада живи у градовима, јавни транспорт и обновљива енергија постају све важнији, као и развој нових индустрија и информационих и комуникационих технологија. Промовисање одрживих грана индустрије и улагање у научна истраживања и иновације су веома важни у циљу обезбеђивања одрживог развоја. Више од 4 милијарде људи још увек нема приступ интернету, а 90 процената од овог броја их живи у земљама у развоју."
            }   
		}   
      }
  },
  {
      "name" : "REDUCED INEQUALITIES",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(10),
          goal:  "Reduce inequality within and among countries",
          desc: "Income inequality is on the rise, with the richest 10 percent earning up to 40 percent of total global income. The poorest 10 percent earn only between 2 percent and 7 percent of total global income. In developing countries, inequality has increased by 11 percent if we take into account the growth of population."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "СМАЊЕНА НЕЈЕДНАКОСТ",
            dataContent: {
          		goal:  "Смањити неједнакост унутар земаља и на интернационалном плану",
            	desc: "Неједнакост у погледу личног дохотка је у порасту, тако да 10 процената најбогатијег становништва зарађује до 40 посто укупне глобалне зараде. Десет процената најсиромашнијих зарађују свега између 2 и 7 посто укупне глобалне зараде. У земљама у развоју неједнакост је порасла за 11 процената ако се узме у обзир пораст популације."
            }   
		}   
      }
  },
  {
      "name" : "SUSTAINABLE CITIES AND COMMUNITIES",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(11),
          goal:  "Make cities inclusive, safe, resilient and sustainable",
          desc: "More than half of the world’s population now live in urban areas. By 2050, it will have risen to two-thirds of all humanity. Sustainable development cannot be achieved without significantly transforming the way we build and manage urban spaces. Extreme poverty is often concentrated in urban spaces, and national and city governments struggle to accommodate the rising population in these areas."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ОДРЖИВИ ГРАДОВИ И ЗАЈЕДНИЦЕ",
            dataContent: {
          		goal:  "Учинити градове инклузивним, безбедним, стабилним и одрживим",
            	desc: "Више од половине светске популације сада живи у урбаним срединама. До 2050. године овај број ће се повећати на две трећине укупног човечанства. Одрживи развој се не може постићи без значајније трансформације начина на који се обавља изградња и управљање урбаним простором. Екстремно сиромаштво је често концентрисано у урбаним срединама, а државне и градске власти се боре да обезбеде одговарајући смештај растућем становништву у овим областима."
            }   
		}   
      }
  },
  {
      "name" : "RESPONSIBLE PRODUCTION AND CONSUMPTION",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(12),
          goal:  "Ensure sustainable consumption and production patterns",
          desc: "Agriculture is the biggest user of water worldwide, and irrigation now claims close to 70 percent of all freshwater for human use. The efficient management of the way we dispose of toxic waste and pollutants, are important targets to achieve this goal. Encouraging industries, businesses and consumers to recycle and reduce waste is equally important."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ОДГОВОРНА ПОТРОШЊА И ПРОИЗВОДЊА",
            dataContent: {
          		goal:  "Обезбедити одрживе моделе потрошње и производње",
            	desc: "Пољопривреда је највећи потрошач воде широм света, а на наводњавање одлази близу 70 посто свих водених ресурса за људску употребу. Ефикасно управљање системима за одлагање токсичног отпада и загађујућих материја представља важне параметре за постизање овог циља. Од једнаког је значаја и подстицање индустрије, предузећа и потрошача да рециклирају и смањују количину произведеног отпада."
            }   
		}   
      }
  },
  {
      "name" : "CLIMATE ACTION",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(13),
          goal:  "Take urgent action to combat climate change and its impacts",
          desc: "Greenhouse gas emissions continue to rise, and are now more than 50 percent higher than their 1990 level. While Eastern Europe and Central Asia is not a big producer of greenhouse gas emissions, the region is suffering disproportionately from the consequences of climate change. Floods in the Western Balkans have destroyed homes and displaced thousands of people."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "КЛИМАТСКЕ АКЦИЈЕ",
            dataContent: {
          		goal:  "Предузети хитне мере у борби с климатским променама и њиховим последицама",
            	desc: "Емисија  гасова са ефектом стаклене баште наставља да расте, и сада је више од 50 процената већа од нивоа из 1990. године. Док источна Европа и централна Азија нису велики емитери гасова с ефектом стаклене баште, ови региони трпе несразмерне последице климатских промена.Поплаве на западном Балкану уништиле су домове и раселиле хиљаде људи."
            }   
		}   
      }
  },
  {
      "name" : "LIFE BELOW WATER",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(14),
          goal:  "Conserve and sustainably use the oceans, seas and marine resources",
          desc: "Over three billion people depend on marine and coastal biodiversity for their livelihoods. However, today we are seeing 30 percent of the world’s fish stocks overexploited, reaching below the level at which they can produce sustainable yields. Marine pollution, an overwhelming majority of which comes from land-based sources, is reaching alarming levels, with an average of 13,000 pieces of plastic litter to be found on every square kilometre of ocean."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ВОДЕНИ ЖИВОТ",
            dataContent: {
          		goal:  "Очувати и на одржив начин користити океане, мора и морске ресурсе",
            	desc: "Више од три милијарде људи зависи од морског и приобалног биодиверзитета како би обезбедили средства за живот. Међутим, данас смо сведоци чињенице да је  30% светских залиха рибе прекомерно експлоатисано, што за последицу има да је њихов број пао испод нивоа на ком оне могу обезбедити одрживу бројност. Загађење мора које у највећој мери потиче од копнених извора достиже алармантне нивое, са просеком од 13.000 комада пластичног отпада на сваком квадратном километру океана."
            }   
		}   
      }
  },
  {
      "name" : "LIFE ON LAND",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(15),
          goal:  "Sustainably manage forests, combat desertification, halt and reverse land degradation, halt biodiversity loss",
          desc: "Today we are seeing unprecedented land degradation, and the loss of arable land at 30 to 35 times the historical rate. Drought and desertification is also on the rise each year, amounting to the loss of 12 million hectares and affects poor communities globally. Of the 8,300 animal breeds known, 8 percent are extinct and 22 percent are at risk of extinction."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ЖИВОТ НА ЗЕМЉИ",
            dataContent: {
          		goal:  "Управљати шумама на одржив начин, борити се против опустињавања, зауставити и вратити уназад процес деградације земљишта, зауставити губитак биодиверзитета",
            	desc: "У данашње време сведоци смо деградације земљишта без преседана и губитка обрадивог земљишта 30 до 35 пута брже него икад у историји. Суша и опустињавање такође су у порасту сваке године, што достиже губитак од чак 12 милиона хектара и погађа сиромашне заједнице на глобалном нивоу. Од познатих 8,300 животињских врста, изумрло је 8 посто, а 22 посто су у ризику од изумирања."
            }   
		}   
      }
  },
  {
      "name" : "PEACE, JUSTICE AND STRONG INSTITUTIONS",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(16),
          goal:  "Promote just, peaceful and inclusive societies",
          desc: "We are living in a world that is increasingly divided. Some regions enjoy sustained levels of peace, security and prosperity, others fall into seemingly endless cycles of conflict and violence. Armed violence and insecurity have a destructive impact on a country’s development, affecting economic growth and often resulting in long standing grievances that can last for generations. Sexual violence, crime, exploitation and torture are also prevalent where there is conflict or no rule of law."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "МИР, ПРАВДА И СНАЖНЕ ИНСТИТУЦИЈЕ",
            dataContent: {
          		goal:  "Промовисати праведно, мирно и инклузивно друштвено окружење",
            	desc: "Живимо у свету који је све више подељен. Неки региони уживају одрживе нивое мира, сигурности и просперитета, док други упадају у наизглед бескрајне циклусе сукоба и насиља. Оружани сукоби  и несигурност имају разоран утицај на развој земље, утичући на економски раст и често резултирајући дуготрајним непријатељствима које могу трајати генерацијама. Сексуално насиље, криминал, експлоатација и мучење су такође присутни када постоји сукоб или нема владавина права."
            }   
		}   
      }
  },
  {
      "name" : "PARTNERSHIPS FOR THE GOALS",
      "iAmId" : ObjectId("556760847125996dc1a4a24f"),
      "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
      "type" : "const.sdgs.sdg",
      "dataContent" : {
          "humanID" : NumberInt(17),
          goal:  "Revitalize the global partnership for sustainable development",
          desc: "The SDGs can only be realized with a strong commitment to global partnership and cooperation. Humanitarian crises brought on by conflict or natural disasters continue to demand more financial resources and aid. Many countries also require Official Development Assistance to encourage growth and trade. The world today is more interconnected than ever before. Improving access to technology and knowledge is an important way to share ideas and foster innovation."
      },
      "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
      "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
      "visual" : {
          "isOpen" : false
      },
      "isPublic" : true,
      "version" : NumberInt(1),
      "activeVersion" : NumberInt(1),
      "__v" : NumberInt(0),
      i18n: {
        rs: {
        	name: "ПАРТНЕРСТВА ЗА ОСТВАРЕЊЕ ЦИЉЕВА",
            dataContent: {
          		goal:  "Подстаћи глобалну сарадњу у домену одрживог развоја",
            	desc: "Циљеви одрживог развоја се могу реализовати само уз снажну посвећеност глобалном партнерству и сарадњи. Хуманитарне кризе изазване сукобима или природним непогодама и даље захтевају више финансијских средстава и помоћи. Многе земље такође захтевају Службу развојне помоћи за подстицање раста и трговине. Данас је свет међусобно повезан више него икада раније. Побољшање приступа технологији и знању је важан начин за размену идеја и подстицање иновација."
            }   
		}   
      }
  }    
]
```

**Edges:**

Add SDG edges in `kedges`  (`right button > Paste document(s)...`):

```json
[
  {
    "_id" : ObjectId("5b4b22d900ea790a4738a705"),
    "name" : "SDG",
    "type" : "const.sdgs.sdg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b9669e986f3cc8057216a15"),
    "targetId" : ObjectId("5b96cb8886f3cc8057216a37"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
  },
  {
    "_id" : ObjectId("5b4b22fd00ea790a4738a706"),
    "name" : "SDG",
    "type" : "const.sdgs.sdg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b9669e986f3cc8057216a15"),
    "targetId" : ObjectId("5b96cb8986f3cc8057216a38"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
  },
  {
    "_id" : ObjectId("5b4b231e00ea790a4738a707"),
    "name" : "SDG",
    "type" : "const.sdgs.sdg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b9669e986f3cc8057216a15"),
    "targetId" : ObjectId("5b96cb8986f3cc8057216a39"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
  },
  {
    "_id" : ObjectId("5b4d105a280f6211059ff60c"),
    "name" : "SDG",
    "type" : "const.sdgs.sdg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b9669e986f3cc8057216a15"),
    "targetId" : ObjectId("5b96cb8986f3cc8057216a3a"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
  },
  {
    "_id" : ObjectId("5b4d105a280f6211059ff60c"),
    "name" : "SDG",
    "type" : "const.sdgs.sdg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b9669e986f3cc8057216a15"),
    "targetId" : ObjectId("5b96cb8986f3cc8057216a3b"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
  },
  {
    "_id" : ObjectId("5b4d105a280f6211059ff60c"),
    "name" : "SDG",
    "type" : "const.sdgs.sdg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("556760847125996dc1a4a24f"),
    "ideaId" : NumberInt(0),
    "sourceId" : ObjectId("5b9669e986f3cc8057216a15"),
    "targetId" : ObjectId("5b96cb8986f3cc8057216a3c"),
    "dataContent" : null,
    "visual" : null,
    "updatedAt" : ISODate("2018-09-10T01:25:34.934+0000"),
    "createdAt" : ISODate("2018-09-10T01:25:34.933+0000"),
    "value" : NumberInt(0),
    "isPublic" : true,
    "__v" : NumberInt(0)
  }
]

/* add remaining edges */
```

## Opening Cards

### SDG Questions

#### Nodes

```
[
    {
          "name" : "How the future looks when this goal is fulfilled?",
          "iAmId" : ObjectId("556760847125996dc1a4a24f"),
          "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
          "type" : "const.dialogame.opening-card",
          "dataContent" : {
              "humanID" : NumberInt(1),
              img: "assets/images/sdgs/m/sdg1.jpg"
          },
          "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
          "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
          "visual" : {
              "isOpen" : true
          },
          "isPublic" : true,
          "version" : NumberInt(1),
          "activeVersion" : NumberInt(1),
          "__v" : NumberInt(0),
          i18n: {
            rs: {
                name: "Како изгледа будућност када је овај циљ испуњен"
            }   
          }
      },
      {
          "name" : "How the future looks when this goal is fulfilled?",
          "iAmId" : ObjectId("556760847125996dc1a4a24f"),
          "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
          "type" : "const.dialogame.opening-card",
          "dataContent" : {
              "humanID" : NumberInt(2),
              img: "assets/images/sdgs/m/sdg2.jpg"
          },
          "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
          "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
          "visual" : {
              "isOpen" : true
          },
          "isPublic" : true,
          "version" : NumberInt(1),
          "activeVersion" : NumberInt(1),
          "__v" : NumberInt(0),
          i18n: {
            rs: {
                name: "Како изгледа будућност када је овај циљ испуњен"
            }   
          }
      },
      {
          "name" : "How the future looks when this goal is fulfilled?",
          "iAmId" : ObjectId("556760847125996dc1a4a24f"),
          "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
          "type" : "const.dialogame.opening-card",
          "dataContent" : {
              "humanID" : NumberInt(3),
              img: "assets/images/sdgs/m/sdg3.jpg"
          },
          "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
          "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
          "visual" : {
              "isOpen" : true
          },
          "isPublic" : true,
          "version" : NumberInt(1),
          "activeVersion" : NumberInt(1),
          "__v" : NumberInt(0),
          i18n: {
            rs: {
                name: "Како изгледа будућност када је овај циљ испуњен"
            }   
          }
      },
      {
          "name" : "How the future looks when this goal is fulfilled?",
          "iAmId" : ObjectId("556760847125996dc1a4a24f"),
          "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
          "type" : "const.dialogame.opening-card",
          "dataContent" : {
              "humanID" : NumberInt(4),
              img: "assets/images/sdgs/m/sdg4.jpg"
          },
          "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
          "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
          "visual" : {
              "isOpen" : true
          },
          "isPublic" : true,
          "version" : NumberInt(1),
          "activeVersion" : NumberInt(1),
          "__v" : NumberInt(0),
          i18n: {
            rs: {
                name: "Како изгледа будућност када је овај циљ испуњен"
            }   
          }
      },
      {
          "name" : "How the future looks when this goal is fulfilled?",
          "iAmId" : ObjectId("556760847125996dc1a4a24f"),
          "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
          "type" : "const.dialogame.opening-card",
          "dataContent" : {
              "humanID" : NumberInt(5),
              img: "assets/images/sdgs/m/sdg5.jpg"
          },
          "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
          "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
          "visual" : {
              "isOpen" : true
          },
          "isPublic" : true,
          "version" : NumberInt(1),
          "activeVersion" : NumberInt(1),
          "__v" : NumberInt(0),
          i18n: {
            rs: {
                name: "Како изгледа будућност када је овај циљ испуњен"
            }   
          }
      },
      {
          "name" : "How the future looks when this goal is fulfilled?",
          "iAmId" : ObjectId("556760847125996dc1a4a24f"),
          "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
          "type" : "const.dialogame.opening-card",
          "dataContent" : {
              "humanID" : NumberInt(6),
              img: "assets/images/sdgs/m/sdg6.jpg"
          },
          "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
          "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
          "visual" : {
              "isOpen" : true
          },
          "isPublic" : true,
          "version" : NumberInt(1),
          "activeVersion" : NumberInt(1),
          "__v" : NumberInt(0),
          i18n: {
            rs: {
                name: "Како изгледа будућност када је овај циљ испуњен"
            }   
          }
      },
      {
          "name" : "How the future looks when this goal is fulfilled?",
          "iAmId" : ObjectId("556760847125996dc1a4a24f"),
          "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
          "type" : "const.dialogame.opening-card",
          "dataContent" : {
              "humanID" : NumberInt(7),
              img: "assets/images/sdgs/m/sdg7.jpg"
          },
          "updatedAt" : ISODate("2018-09-10T20:16:47.306+0000"),
          "createdAt" : ISODate("2018-09-10T20:16:47.301+0000"),
          "visual" : {
              "isOpen" : true
          },
          "isPublic" : true,
          "version" : NumberInt(1),
          "activeVersion" : NumberInt(1),
          "__v" : NumberInt(0),
          i18n: {
            rs: {
                name: "Како изгледа будућност када је овај циљ испуњен"
            }   
          }
      }

]
```

#### Edges

**TODO**

should connect them with **Content (node)** or with **Content (node)** -> **DialoGame**

## Users Population

### **Test Users**

**email**: test_user@gmail.com

**pass**: pass

```JSON
[
    {
        "_id" : ObjectId("5b97c7ab0393b8490bf5263c"),
        "name" : "Test",
        "type" : "rima.user",
        "iAmId" : ObjectId("556760847125996dc1a4a24f"),
        "ideaId" : NumberInt(0),
        "dataContent" : {
            "hash" : "b4523dcbb2c79cb2347abfe3ac1d10d5d831abd664909d7c45a9d296ab9ee96f701894fe29a702984e92ba4d2fa9cda552ab98e06da1244ce644e7866dd80d52",
            "salt" : "480501a1e8fcf0f213a488489c10ea05",
            "email" : "test_user@gmail.com",
            "lastName" : "User",
            "firstName" : "Test"
        },
        "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
        "updatedAt" : ISODate("2018-09-11T13:48:27.641+0000"),
        "createdAt" : ISODate("2018-09-11T13:48:27.624+0000"),
        "visual" : {
            "isOpen" : false
        },
        "isPublic" : true,
        "version" : NumberInt(1),
        "activeVersion" : NumberInt(1),
        "__v" : NumberInt(0)
    },
    {
        "_id" : ObjectId("5b9fbdd97f07953d41256b31"),
        "name" : "Test2",
        "type" : "rima.user",
        "iAmId" : ObjectId("556760847125996dc1a4a24f"),
        "ideaId" : NumberInt(0),
        "dataContent" : {
            "hash" : "b4523dcbb2c79cb2347abfe3ac1d10d5d831abd664909d7c45a9d296ab9ee96f701894fe29a702984e92ba4d2fa9cda552ab98e06da1244ce644e7866dd80d52",
            "salt" : "480501a1e8fcf0f213a488489c10ea05",
            "email" : "test_user2@gmail.com",
            "lastName" : "User",
            "firstName" : "Test2"
        },
        "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
        "updatedAt" : ISODate("2018-09-11T13:48:27.641+0000"),
        "createdAt" : ISODate("2018-09-11T13:48:27.624+0000"),
        "visual" : {
            "isOpen" : false
        },
        "isPublic" : true,
        "version" : NumberInt(1),
        "activeVersion" : NumberInt(1),
        "__v" : NumberInt(0)
    },
    {
        "_id" : ObjectId("5b9fbde97f07953d41256b32"),
        "name" : "Test3",
        "type" : "rima.user",
        "iAmId" : ObjectId("556760847125996dc1a4a24f"),
        "ideaId" : NumberInt(0),
        "dataContent" : {
            "hash" : "b4523dcbb2c79cb2347abfe3ac1d10d5d831abd664909d7c45a9d296ab9ee96f701894fe29a702984e92ba4d2fa9cda552ab98e06da1244ce644e7866dd80d52",
            "salt" : "480501a1e8fcf0f213a488489c10ea05",
            "email" : "test_user3@gmail.com",
            "lastName" : "User",
            "firstName" : "Test3"
        },
        "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
        "updatedAt" : ISODate("2018-09-11T13:48:27.641+0000"),
        "createdAt" : ISODate("2018-09-11T13:48:27.624+0000"),
        "visual" : {
            "isOpen" : false
        },
        "isPublic" : true,
        "version" : NumberInt(1),
        "activeVersion" : NumberInt(1),
        "__v" : NumberInt(0)
    },
    {
        "_id" : ObjectId("5b9fbde97f07953d41256b33"),
        "name" : "Test4",
        "type" : "rima.user",
        "iAmId" : ObjectId("556760847125996dc1a4a24f"),
        "ideaId" : NumberInt(0),
        "dataContent" : {
            "hash" : "b4523dcbb2c79cb2347abfe3ac1d10d5d831abd664909d7c45a9d296ab9ee96f701894fe29a702984e92ba4d2fa9cda552ab98e06da1244ce644e7866dd80d52",
            "salt" : "480501a1e8fcf0f213a488489c10ea05",
            "email" : "test_user4@gmail.com",
            "lastName" : "User",
            "firstName" : "Test4"
        },
        "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
        "updatedAt" : ISODate("2018-09-11T13:48:27.641+0000"),
        "createdAt" : ISODate("2018-09-11T13:48:27.624+0000"),
        "visual" : {
            "isOpen" : false
        },
        "isPublic" : true,
        "version" : NumberInt(1),
        "activeVersion" : NumberInt(1),
        "__v" : NumberInt(0)
    }
]
```

## Mockup Data

### My CWC-Chat Dreams

```JSON
[
 {
    "name" : "sun is always here",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b97c7ab0393b8490bf5263c"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "name" : "girls are playing in the garden",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b97c7ab0393b8490bf5263c"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "name" : "love is here",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b97c7ab0393b8490bf5263c"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
  {
    "name" : "green parks for every building",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b97c7ab0393b8490bf5263c"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
 {
    "name" : "water for each child is more important than profit",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b97c7ab0393b8490bf5263c"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
}
]
```

### Others CWC-Chat Dreams played as Responses

```JSON
[
 {
     "_id" : ObjectId("5b9fc0e17f07953d41256b44"),
    "name" : "running over fields full of food",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbdd97f07953d41256b31"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b45"),
    "name" : "yellow wheats on hills",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbdd97f07953d41256b31"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b46"),
    "name" : "books are free for every child in this planet",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbdd97f07953d41256b31"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8280"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b47"),
    "name" : "women have rights as equal workers",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbdd97f07953d41256b31"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b48"),
    "name" : "fish swim in plasti-free oceans",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbdd97f07953d41256b31"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b49"),
    "name" : "people enjoy in smelly seaside",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbdd97f07953d41256b31"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b4a"),
    "name" : "justice is unquestionable",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbde97f07953d41256b32"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b4b"),
    "name" : "every company has a recycling system",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbde97f07953d41256b32"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b4c"),
    "name" : "renewable energy is the only energy",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbde97f07953d41256b32"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b4d"),
    "name" : "every family has a minimum salary",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbde97f07953d41256b32"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(1), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
{
    "_id" : ObjectId("5b9fc0e17f07953d41256b4e"),
    "name" : "elementary school is free for every child",
    "type" : "topiChat.talk.chatMsg",
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"),
    "iAmId" : ObjectId("5b9fbde97f07953d41256b32"),
    "ideaId" : NumberInt(0),
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"),
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"),
     "dataContent" : {
        "dialoGameReponse" : {
            "playRound" : NumberInt(2), 
            "challengeCards" : [
                "5b978bba86f3cc9a70dd8277"
            ], 
            "decorators" : [

            ]
        }
    }, 
    "visual" : {
        "isOpen" : true
    },
    "isPublic" : true,
    "version" : NumberInt(1),
    "activeVersion" : NumberInt(1),
    "__v" : NumberInt(0)
},
]
```

### Suggested Cards from Service



```json
{ 
    "_id" : ObjectId("5ba10aa6f8b8e4270c371eae"), 
    "name" : "Suggested CWC Cards from Service", 
    "type" : "service.result.dialogame.cwc_similarities", 
    "mapId" : ObjectId("5b96619b86f3cc8057216a03"), 
    "iAmId" : ObjectId("5b97c7ab0393b8490bf5263c"), 
    "ideaId" : NumberInt(0), 
    "updatedAt" : ISODate("2018-09-10T01:18:20.440+0000"), 
    "createdAt" : ISODate("2018-09-10T01:18:20.439+0000"), 
    "visual" : {
        "isOpen" : true
    }, 
    "dataContent" : {
        "result" : {
            "suggestions" : [
                {
                    "id" : "5b9fc0e17f07953d41256b45", 
                    "similarity_quotient" : 0.9
                }, 
                {
                    "id" : "5b9fc0e17f07953d41256b46", 
                    "similarity_quotient" : 0.4
                }, 
                {
                    "id" : "5b9fc0e17f07953d41256b48", 
                    "similarity_quotient" : 0.8
                }, 
                {
                    "id" : "5b9fc0e17f07953d41256b4a", 
                    "similarity_quotient" : 0.2
                }, 
                {
                    "id" : "5b9fc0e17f07953d41256b4e", 
                    "similarity_quotient" : 0.35
                }
            ], 
            "gameRound" : 1.0
        }
    }, 
    "isPublic" : true, 
    "version" : NumberInt(1), 
    "activeVersion" : NumberInt(1), 
    "__v" : NumberInt(0)
}
```