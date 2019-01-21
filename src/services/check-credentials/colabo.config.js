var puzzles = {
    name: "@ace-mediator/service-check-credentials",
    description: "A ColaboFlow (CF) Go service checking user credentials",
    dependencies: {
        "@colabo-flow/i-audit": {},
        "@colabo-flow/b-audit": {},
        "@colabo-flow/s-audit": {},

        "@colabo-flow/i-go": {},
        "@colabo-flow/b-go": {},
        "@colabo-flow/s-go": {},

        "@colabo-utils/i-config": {}
    },
    offers: {}
}

exports.puzzles = puzzles;