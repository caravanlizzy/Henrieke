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
        result => {
            this.getGame(gameId, playerId, pw);
        })
    }

    createGame(playerId) {
        $.get("php/access.php",
        {
            task: "createGame",
            playerId: playerId
        }, 
        result => {
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
            this.getGame(gameId, playerId, pw);
        })
    }

    getGame(gameId, playerId, pw) {
        $.get("php/access.php",
        {
            task: "getGame",
            gameId: gameId,
            playerId: playerId,
            pw: pw
        },
        result => {
            let playerIds = this.game.getPlayerIds();
            let playerInfos = this.game.decodeGame(result);
            for(let i = 0; i < playerInfos.length; i++) {
                let playerInfo = playerInfos[i];
                let playerId = parseInt(playerInfo[0]);
                let nick = playerInfo[1];
                let playedCard = playerInfo[2];
                let deck = playerInfo[3];
                let crowns = playerInfo[4];
                if(playerIds.indexOf(playerId) < 0) {
                    this.game.addPlayer(playerId, nick);
                } 
                let player = this.game.getPlayer(playerId);
                if(playedCard != '11') {
                    player.hasPlayed = true;
                    this.game.graphic.updateCardDisplay(playerId, "X");
                }
                for(let j = 0; j < deck.length; j++) {
                    if(deck[j] == '0'){
                        player.removeCard(j);
                    }
                }
                player.updateCrowns(crowns);
            }
            this.game.updateGraphics();
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

    removeGame(gameId, playerId, pw) {
        $.get("php/access.php", {
            task: "removeGame",
            gameId: gameId,
            playerId: playerId,
            pw: pw
        },
        result => {
            this.getGame(gameId, playerId, pw);
        });
    }

    
}