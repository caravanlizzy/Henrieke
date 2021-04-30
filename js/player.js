class Player{
    constructor(name) {
        this.name = name;
        this.cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        this.crowns = 0;
        this.host = false;
    }

    sethost() {
        this.host = true;
    }

    unsethost() {
        this.host = false;
    }

    setname(newName) {
        this.name = newName;
    }

    addcrown() {
        this.crowns += 1;
    }

    reset() {
        this.cards = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        this.crowns = 0;
    }


}