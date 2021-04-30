class Graphic {
    // constructor() {
    //     this.playertableaus = [];
    // }
    drawbox(classname, id, parente) {
        let box = document.createElement("div");
        box.className = classname;
        box.id = id;
        parente.append(box);
        return box;
    }

    drawmainframe() {
        this.drawbox("mainframe", "mainframe", document.body);
    }

    drawplayertableau(playerid) {
        let playertableau = this.drawbox("playertableau", "playertableau" + playerid, document.getElementById("mainframe"));
        this.playertableaus.push(playertableau);
        this.drawplayerinfo(playerid, "testname");
        this.drawcardsbox(playerid);
        this.drawdiscardbox(playerid);
        this.drawcarddisplaybox(playerid);
        this.drawcrownsbox(playerid);
    }

    getplayertableau(playerid) {
        return document.getElementById("playertableau" + playerid);
    }

    drawplayerinfo(playerid, name) {
        let classname = "playerinfo";
        let playerinfo = this.drawbox(classname, classname + playerid, this.getplayertableau(playerid));
        let textbox = document.createElement("div");
        textbox.innerHTML = name;
        playerinfo.append(textbox);
    }

    updateplayerinfo(playerid, newname) {
        let playerinfo = document.getElementById("playerinfo" + playerid);
        playerinfo.innerHTML = newname;
    }

    drawcardsbox(playerid) {
        let classname = "cardbox";
        let cardbox = this.drawbox(classname, classname + playerid, this.getplayertableau(playerid));
        this.drawbox("zerobox", "zerobox" + playerid, cardbox);
        this.drawbox("nonzerobox", "nonzerobox" + playerid, cardbox);
    }

    drawcard(playerid, card, color) {
        let classname = "card";
        let id = classname + card + "p" + playerid;
        let parentboxname = (card == 0 ? "zerobox" : "nonzerobox");
        let c = this.drawbox(classname + " " + color + " " + "small", id, document.getElementById(parentboxname + playerid)); 
        c.innerHTML = card;
    }

    deletecard(playerid, card) {
        let id = "card" + card + "p" + playerid;
        let c = document.getElementById(id);
        c.parentNode.removeChild(c);
    }

    drawdiscardbox(playerid) {
        let classname = "discardbox";
        this.drawbox(classname, classname + playerid, this.getplayertableau(playerid));
    }

    drawdiscard(playerid, card, color) {
        let classname = "discard";
        let id = classname + card + "p" + playerid;
        let c = this.drawbox(classname + " " + color + " " + "small", id, document.getElementById("discardbox" + playerid));
        c.innerHTML = card;
    }

    deletediscard(playerid, discard) {
        let id = "discard" + discard + "p" + playerid;
        let dc = document.getElementById(id);
        dc.parentNode.removeChild(dc); 
    }

    drawcrownsbox(playerid) {
        let classname = "crownbox";
        this.drawbox(classname, classname + playerid, this.getplayertableau(playerid));
    }

    updatecrowns(playerid, crowns) {
        document.getElementById("crownbox" + playerid).innerHTML = crowns;
    }

    drawcarddisplaybox(playerid) {
        let classname = "carddisplaybox";
        this.drawbox(classname, classname + playerid, this.getplayertableau(playerid));
    }

    drawboards(players) {
        let nplayers = players.length;
        for (let i = 0; i < nplayers; i++) {
            this.drawplayertableau(i);
        }
    }


}