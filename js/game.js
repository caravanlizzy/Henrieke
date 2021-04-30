class Game{
    constructor() {
        this.players = [];
        this.graphic = new Graphic();
    }

    addPlayer(name) {
        let newPlayer = new Player(name);
    }

    setupGraphic() {
        this.graphic.drawMainFrame();
        this.graphic.drawStatusBar();
    }
}