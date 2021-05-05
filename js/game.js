class Game{
    constructor(gameId) {
        this.players = [];
        this.gameId = gameId;
        this.graphic = new Graphic(this);
        this.request = new Request(this);

    }

    addPlayer(name, playerId) {
        let newPlayer = new Player(name, playerId);
        this.players.push(newPlayer);
    }

    checkId() {
        
    }

    createGame() {
        this.request.createGame();
    }

    startGame() {
        this.request.startGame();
    }

    setupGraphic() {
        this.graphic.drawMainFrame();
        this.graphic.drawStatusBar();
        this.drawBoards();
        this.drawCards();
    }

    drawBoards() {
        this.players.forEach(player => {
            this.graphic.drawPlayerTableau(player.id, player.name);
        })        
    }

    drawCards() {
        this.players.forEach(player => {
            player.cards.forEach(card => {
                this.graphic.drawCard(player.id, card, player.color);
            })
        })
    }
    getCards() {
        this.request.getCards();
    }
}