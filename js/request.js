class Request{
    constructor(game) {
        this.gameId = 0;
        this.game = game;
        // this.test = 0;
        // this.cardResponse = null;
        // return;
    }

    getGameId() {
        return this.gameId;
    }

    playCard(gameId, playerId, card) {
        $.get("php/access.php",
        {
            task: "playCard",
            playerId: playerId,
            gameId: gameId,
            card: card
        }, 
        function(result) {
            // alert(result);
            alert("played card: " + result);
        })
    }

    createGame() {
        $.get("php/access.php",
        {
            task: "createGame"
        }, 
        result => {
            this.game.gameId = parseInt(result);
        })
    }


    startGame(gameId) {
        $.get("php/access.php",
        {
            task: "startGame",
            gameId: gameId
        }, 
        result => {
            return;
        })
    }

    joinGame(gameId, nick) {
        $.get("php/access.php",
        {
            task: "joinGame",
            nick: nick,
            gameId: gameId
        },
        function(result) {
            alert(result);
        })
    }

    getCards(gameId) {
        $.get("php/access.php",
        {
            task: "getCards",
            gameId: gameId
        },
        function(result) {
            alert(result);
        }) 
    }
}