# Performing Sustainable CoEvolution (PSC)
(developed upon ***CoLaboArthon***, ***DialoGame***, and ***CoEvoLudens*** formats)

- a standalone **app** for promoting and initiating '**Doug Engelbart's CoEvolution**'
- the app is built to support the workshop with the same name

## entry points

+ http://localhost:8891

# Workshop Procedure

https://github.com/Cha-OS/colabo/issues/325

## Intro Video

- **ISSUES**
  - https://github.com/Cha-OS/colabo/issues/314

## Registration

- name, email, pass
- **ISSUES**
  - https://github.com/Cha-OS/colabo/issues/299
  - https://github.com/Cha-OS/colabo/issues/296

## SDG Selection

- helps in opening views of participants
- helps in personalization of procedures by tagging them with 3 of 17 **UN SDGs**
- demonstrates clustering (group forming) to participants
- we can finish with taking **SDG Avatar** and saving it to our profile
- **ISSUES**
  - https://github.com/Cha-OS/colabo/issues/330
  - https://github.com/Cha-OS/colabo/issues/319
  - https://github.com/Cha-OS/colabo/issues/318
  - https://github.com/Cha-OS/colabo/issues/307
  - 

## CWC Dreaming

- background music
- intro - meditative story - relaxation
- dreaming
- CWCs -> chat 
  - 5 short sentences describing the future
- **ISSUES**
  - https://github.com/Cha-OS/colabo/issues/331

## Playing DialoGame

- **chalenges**
  - at the opening we connect our story with SDG goals - answering on a SDG Question card by our card
  - later we answer on the cards played in the first round
- steps
  - **our system uses ML, NLP, AI to suggest** the most related cards to us (to our cards, to our profile, to our moves)
  - we choose one of the **displayed challenge card **
  - we respond by some of our cards (made out of CWC sentences)
  - we **decorate** our card
  - previewing/checking our move, confirming it
  - the card is **stored** in the game map
  - everybody is **synced** with moves from the current round
  - **new round** is started (there are two rounds for users to play)
- **ISSUES**
  - https://github.com/Cha-OS/colabo/issues/333
  - https://github.com/Cha-OS/colabo/issues/329
  - https://github.com/Cha-OS/colabo/issues/326
  - https://github.com/Cha-OS/colabo/issues/321
  - https://github.com/Cha-OS/colabo/issues/316
  - https://github.com/Cha-OS/colabo/issues/315

## Performance

- SDG question is shown on the screen
- first performer goes out
- the one who answered it goes out
- the third performer (who would play the last card on the card of the 2nd player), plays it by performing it as a continuation of their play
- after they played it in the 1st round, Moderators put Limiting/Guiding Decorators 
- moderators explain them rules, let them think over it **together now, to co-create** it and perform it for the 2nd time

### Moderators put Limiting/Guiding Decorators

#### General

- can be played by moderators by using an **RFID card** of Doug's Dream and Challenge, playing it on the RFID reader and by that decorating the current performance (e.g. the first card in its chain)
- 

#### Doug Engelbart's Co-evolution

#### Real World SDF Challenge Case

**Issues**

- https://github.com/Cha-OS/colabo/issues/327
- https://github.com/Cha-OS/colabo/issues/332

# Structure

## Database

- 17 UN SDGs are connected to the node {"_id" : ObjectId("5b4a91d800ea790a4738a6e5"), "name" : "SDGs", "type" : "const.sdgs"}
- 17 cons SDG nodes are of type "type" : "const.sdgs.sdg"
-

# Install

Before running the App, you need to prepolate the database.

See the [INSTALL](INSTALL.md) file for details.

## Building. CLI

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 1.5.0.

- **Development server**
  Run `ng serve` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.
- **Code scaffolding**
- Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.
- **Build**
  Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `-prod` flag for a production build.
- **Further help**
  To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).

## Testing

- **Running unit tests**
  Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).
- **Running end-to-end tests**
  Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/)
