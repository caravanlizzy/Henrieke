class Game{
    constructor(gameId) {
        this.players = [];
        this.gameId = gameId;
        this.meName = "MyName";
        this.graphic = new Graphic(this);
        this.request = new Request(this);
    }

    createGame() {
        this.request.createGame();
    }

    startGame() {
        let me = this.getMe();
        this.request.startGame(this.gameId, me.id, me.pw);
    }

    getGame() {
        let me = this.getMe();
        this.request.getGame(this.gameId, me.id, me.pw);
    }

    joinGame() {
        let me = this.getMe();
        if(me.inGame) {
            alert("You are already in the game.");
            return;
        }
        this.request.joinGame(this.gameId, this.meName);
    }

    getPlayer(playerId) {
        for(let i = 0; i < this.players.length; i++) {
            if(this.players[i].id == playerId) {
                return this.players[i];
            }
        }
    }

    getPlayerIds() {
        let playerIds = [];
        for(let i = 0; i < this.players.length; i++) {
            playerIds.push(this.players[i].id);
        }
        return playerIds;
    }


    getMe() {
        for(let i = 0; i < this.players.length; i++) {
            let player = this.players[i];
            if(player.me) {
                return player;
            }
        }
        return false;
    }

    
    addPlayer(playerId, nick, pw = false, me = false) {
        // alert(playerId);
        let newPlayer = new Player(playerId, nick, pw, me);
        this.players.push(newPlayer);
        this.graphic.drawPlayerTableau(playerId, nick);
        this.updateCards();
    }

    playCard(playerId, card) {
        let player = this.getPlayer(playerId);
        if(player.pw != false && player.me == true){
            this.request.playCard(this.gameId, player.id, player.pw,  card);
        }
    }

    updateCards() {
        this.players.forEach(player => {
            this.graphic.deleteAllCards(player.id);
            player.cards.forEach(card => {
                this.graphic.drawCard(player.id, card, player.color);
            })
        })
    }

    setupGraphic() {
        this.graphic.drawMainFrame();
        this.graphic.drawStatusBar();
        // this.drawBoards();
        // this.drawCards();
    }

    updateGraphics(display = false) {
        for(let i = 0; i < this.players.length; i++) {
            let player = this.players[i];
            this.graphic.updateCrowns(player.id, player.crowns);
            this.graphic.deleteAllCards(player.id);
            let cards = player.cards;
            for(let j = 0; j < 11; j++) {
                if(j in cards){
                    this.graphic.drawCard(player.id, j, player.color);
                }
            }
        }
    }

    decodeGame(encodedGame) {
        let players = encodedGame.split("-");
        let playerInfos = [];
        for(let i = 0; i < players.length; i++) {
            let playerInfo = players[i].split(":");
            playerInfos.push(playerInfo);
        }
        return playerInfos;
    }

    updateGameState(newState) {
        this.graphic.updateGameState(newState);
    }

    // onEnteringGame() {
    //     return;
    // }

    // onLeavingGame() {
    //     return;
    // }

    // setupGame() {
    //     return;
    // }


}