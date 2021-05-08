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

    playCard(gameId, playerId, pw, card) {
        $.get("php/access.php",
        {
            task: "playCard",
            playerId: playerId,
            gameId: gameId,
            card: card,
            pw: pw
        }, 
        function(result) {
            // alert(result);
            alert("played card: " + result);
        })
    }

    createGame(playerId) {
        $.get("php/access.php",
        {
            task: "createGame",
            playerId: playerId
        }, 
        result => {
            alert(result);
            this.game.gameId = parseInt(result);
        })
    }


    startGame(gameId, playerId, pw) {
        $.get("php/access.php",
        {
            task: "startGame",
            gameId: gameId,
            playerId,
            pw: pw
        }, 
        result => {
            this.game.updateGameState(result);
            // return;
        })
    }

    joinGame(gameId, nick) {
        $.get("php/access.php",
        {
            task: "joinGame",
            nick: nick,
            gameId: gameId
        },
        result => {
            // alert(result);
            let results = result.split("_");
            let playerId = parseInt(results[0]);
            let pw = results[1];
            this.game.addPlayer(playerId, nick, pw, true);
        })
    }

    allCardsPlaced(gameId, playerId, pw) {
        $.get("php/access.php",
        {
            task: "allCardsPlaced",
            gameId: gameId,
            playerId: playerId,
            pw: pw
        },
        result => {
            if(result == 0) {
                return;
            }
            if(result == 1) {
                this.endRound(gameId, playerId, pw);
            }
        }) 
    }

    endRound(gameId, playerId, pw) {
        $.get("php/access.php",
        {
            task: "endRound",
            gameId: gameId,
            playerId: playerId,
            pw: pw
        },
        result => {
            let playerInfos = result.split("-");
            let playerData = [];
            playerInfos.forEach(p => {
                playerData.push(p.split(":"));
            });
            let crowns = [];
            let decks = [];
            playerData.forEach(d => {
                crowns.push(d[0]);
                decks.push(d[1]);
            });
            this.game.updateGraphics(decks, crowns);
        }) 
    }
}