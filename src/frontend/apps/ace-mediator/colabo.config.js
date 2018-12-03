var variables = {
    // ANGULAR_PACKAGES_FOLDER: '/Users/sasha/Documents/data/development/colabo.space/colabo/src/frontend/',
    // ANGULAR_BUILD_PACKAGES_FOLDER: '/Users/sasha/Documents/data/development/colabo.space/colabo/src/frontend/'
    ANGULAR_PACKAGES_FOLDER: '../../../../../../../colabo.space/colabo/src/frontend/',
    ANGULAR_BUILD_PACKAGES_FOLDER: '../../../../../../../colabo.space/colabo/src/frontend/'
};

var puzzles = {
    name: "@ace-apps/f-mediator",
    description: "Audio Commons Ecosystem (ACE) frontend for interaction with mediator",
    sudo: {
        "offer": false,
        "install": false,
        "build": false,
        "symlinks": false
    },
    dependencies: {
        "@colabo-puzzles/f-core": {},
        "@colabo-utils/i-pub-sub": {},
        "@colabo-flow/f-audit": {},
        "@colabo-flow/i-audit": {},
        "@colabo-utils/i-config": {},
        "@colabo-utils/f-notifications": {}
    },
    offers: {}
};

var symlinks = [
    // {
    //     from: variables.ANGULAR_PACKAGES_FOLDER + "node_modules/rxjs",
    //     to: "node_modules/rxjs"
    // },
    // {
    //     from: variables.ANGULAR_PACKAGES_FOLDER + "node_modules/\@angular",
    //     to: "node_modules/\@angular"
    // },
    // {
    //     from: variables.ANGULAR_BUILD_PACKAGES_FOLDER + "node_modules/\@angular-devkit",
    //     to: "node_modules/\@angular-devkit"
    // }
];

exports.variables = variables;
exports.puzzles = puzzles;
exports.symlinks = symlinks;