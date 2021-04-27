class Game{
    constructor() {
        this.players = [];
        this.graphic = new Graphic();
    }

    addplayer(name) {
        let newplayer = new Player(name);
    }

    setupgraphic() {
        this.graphic.drawmainframe();
    }
}