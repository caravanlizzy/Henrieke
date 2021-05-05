class Player{
    constructor(name, playerId) {
        this.name = name;
        this.cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        this.crowns = 0;
        this.color = this.getRandomColor();
        this.host = false;
        this.id = playerId;
        this.key = "";
    }

    setHost() {
        this.host = true;
    }

    unsetHost() {
        this.host = false;
    }

    setName(newName) {
        this.name = newName;
    }

    setCrowns(c) {
        this.crowns = c;
    }

    reset() {
        this.cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        this.crowns = 0;
    }

    getRandomColor() {
        let colors = ["blue", "red", "green", "yellow", "orange", "rose"];
        let index = Math.floor(Math.random() * colors.length);
        return colors[index];
    }


}