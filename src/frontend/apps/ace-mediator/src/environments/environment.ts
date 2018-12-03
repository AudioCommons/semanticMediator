// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
  production: false,

  mapId: '5b96619b86f3cc8057216a03',

  /** multiple players can play on the same opening card */
  OPENNING_CARD_MULTIPLE_ANSWERS: true,

  /** multiple players can play on a card played by another player */
  PLAYER_CARD_MULTIPLE_ANSWERS: true,

  /** multiple players can play on a card played by another player */
  REPLAY_PLAYED_CARD: false
};
