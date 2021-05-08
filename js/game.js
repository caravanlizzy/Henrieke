class Game{
    constructor(gameId) {
        this.players = [];
        this.gameId = gameId;
        this.meName = "MyName";
        this.graphic = new Graphic(this);
        this.request = new Request(this);
    }



    addPlayer(playerId, nick, pw = false, me = false) {
        let newPlayer = new Player(playerId, nick, pw, me);
        this.players.push(newPlayer);
        this.graphic.drawPlayerTableau(playerId, nick);
        this.updateCards();
    }

    joinGame() {
        let me = this.getMe();
        if(me.inGame) {
            alert("You are already in the game.");
            return;
        }
        this.request.joinGame(this.gameId, this.meName);
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

    getPlayer(playerId) {
        for(let i = 0; i < this.players.length; i++) {
            if(this.players[i].id == playerId) {
                return this.players[i];
            }
        }
        // this.players.forEach(p => {
        //     if(p.id == playerId) {
        //         return p;
        //     }
        // })
    }

    createGame() {
        this.request.createGame();
    }

    startGame() {
        let me = this.getMe();
        this.request.startGame(this.gameId, me.id, me.pw);
    }

    setupGraphic() {
        this.graphic.drawMainFrame();
        this.graphic.drawStatusBar();
        // this.drawBoards();
        // this.drawCards();
    }

    updateGameState(newState) {
        this.graphic.updateGameState(newState);
    }

    updateCards() {
        this.players.forEach(player => {
            this.graphic.deleteAllCards(player.id);
            player.cards.forEach(card => {
                this.graphic.drawCard(player.id, card, player.color);
            })
        })
    }

    playCard(playerId, card) {
        let player = this.getPlayer(playerId);
        this.request.playCard(this.gameId, player.id, player.pw,  card);
    }

    updateGraphics(decks, crowns) {
        for(let i = 0; i < crowns.length; i++) {
            let player = this.players[i];
            this.graphic.updateCrowns(player.id, crowns[i]);
            this.graphic.deleteAllCards(player.id);
            let deck = decks[i];
            let cards = this.getCardsFromDeck(deck);
            for(let j = 0; j < 11; j++) {
                if(j in cards){
                    this.graphic.drawCard(player.id, j, player.color);
                } else {
                    this.graphic.drawDiscard(player.id, j, player.color);
                }
            }
        }
    }

    getCardsFromDeck(deck){
        let cards = [];
        for(let i = 0; i < deck.length; i++){
            if(deck[i] == '1'){
                cards.push(i);
            }
        }
        return cards;
    }

    allCardsPlaced() {
        let me = this.getMe();
        this.request.allCardsPlaced(this.gameId, me.id, me.pw);
    }
}