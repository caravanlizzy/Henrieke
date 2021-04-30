class Graphic {

    drawBox(className, id, parente) {
        let box = document.createElement("div");
        box.className = className;
        box.id = id;
        parente.append(box);
        return box;
    }

    drawMainFrame() {
        this.drawBox("mainFrame", "mainFrame", document.body);
    }

    getMainFrame() {
        return document.getElementById("mainFrame");
    }

    drawPlayerTableau(playerId) {
        let playerTableau = this.drawBox("playerTableau", "playerTableau" + playerId, this.getMainFrame());
        // this.playerTableaus.push(playerTableau);
        this.drawPlayerInfo(playerId, "testname");
        this.drawCardsBox(playerId);
        this.drawDiscardBox(playerId);
        this.drawCardDisplayBox(playerId);
        this.drawCrownsBox(playerId);
    }

    getPlayerTableau(playerId) {
        return document.getElementById("playerTableau" + playerId);
    }

    drawPlayerInfo(playerId, name) {
        let className = "playerInfo";
        let playerInfo = this.drawBox(className, className + playerId, this.getPlayerTableau(playerId));
        let textBox = document.createElement("div");
        textBox.innerHTML = name;
        playerInfo.append(textBox);
    }

    updateplayerInfo(playerId, newName) {
        let playerInfo = document.getElementById("playerInfo" + playerId);
        playerInfo.innerHTML = newName;
    }

    drawCardsBox(playerId) {
        let className = "cardBox";
        let cardBox = this.drawBox(className, className + playerId, this.getPlayerTableau(playerId));
        this.drawBox("zeroBox", "zeroBox" + playerId, cardBox);
        this.drawBox("nonZeroBox", "nonZeroBox" + playerId, cardBox);
    }

    drawcard(playerId, card, color) {
        let className = "card";
        let id = className + card + "p" + playerId;
        let parentBoxName = (card == 0 ? "zeroBox" : "nonZeroBox");
        let c = this.drawBox(className + " " + color + " " + "small", id, document.getElementById(parentBoxName + playerId)); 
        c.innerHTML = card;
    }

    deletecard(playerId, card) {
        let id = "card" + card + "p" + playerId;
        let c = document.getElementById(id);
        c.parentNode.removeChild(c);
    }

    drawDiscardBox(playerId) {
        let className = "discardBox";
        this.drawBox(className, className + playerId, this.getPlayerTableau(playerId));
    }

    drawdiscard(playerId, card, color) {
        let className = "discard";
        let id = className + card + "p" + playerId;
        let c = this.drawBox(className + " " + color + " " + "small", id, document.getElementById("discardBox" + playerId));
        c.innerHTML = card;
    }

    deletediscard(playerId, discard) {
        let id = "discard" + discard + "p" + playerId;
        let dc = document.getElementById(id);
        dc.parentNode.removeChild(dc); 
    }

    drawCrownsBox(playerId) {
        let className = "crownBox";
        this.drawBox(className, className + playerId, this.getPlayerTableau(playerId));
    }

    updatecrowns(playerId, crowns) {
        document.getElementById("crownBox" + playerId).innerHTML = crowns;
    }

    drawCardDisplayBox(playerId) {
        let className = "cardDisplayBox";
        this.drawBox(className, className + playerId, this.getPlayerTableau(playerId));
    }

    drawBoards(players) {
        let nplayers = players.length;
        for (let i = 0; i < nplayers; i++) {
            this.drawPlayerTableau(i);
        }
    }

    drawStatusBar() {
        let className = "statusBar";
        this.drawBox(className, className, this.getMainFrame())
    }

}