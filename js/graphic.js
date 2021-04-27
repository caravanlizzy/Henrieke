class Graphic{
    constructor(){
        this.playertableaus = [];
    }

    drawbox(classname, id, parente){
        let box = document.createElement("div");
        box.className = classname;
        box.id = id;
        parente.append(box);
        return box;
    }

    drawmainframe(){
        this.drawbox("mainframe", "mainframe", document.body);
    }

    drawplayertableau(playerid){
        let playertableau = this.drawbox("playertableau", "playertableau" + playerid, document.getElementById("mainframe"));
        this.playertableaus.push(playertableau);
        this.drawplayerinfo(playerid, "testname");
        this.drawcardsbox(playerid);
        this.drawdiscardbox(playerid);
        this.drawcrownsbox(playerid);
        this.drawcarddisplaybox(playerid);
    }

    getplayertableau(playerid){
        return document.getElementById("playertableau" + playerid);
    }

    drawplayerinfo(playerid, name){
        let classname = "playerinfo";
        let playerinfo = this.drawbox(classname, classname + playerid, this.getplayertableau(playerid));
        let textbox = document.createElement("div");
        textbox.innerHTML = name;
        playerinfo.append(textbox);
    }

    updateplayerinfo(playerid, newname){
        let playerinfo = document.getElementById("playerinfo" + playerid);
        playerinfo.innerHTML = newname;
    }

    drawcardsbox(playerid){
        let classname = "cardbox";
        this.drawbox(classname, classname+playerid, this.getplayertableau(playerid));
    }

    drawdiscardbox(playerid){
        let classname = "discardbox";
        this.drawbox(classname, classname+playerid, this.getplayertableau(playerid));
    }

    drawcrownsbox(playerid){
        let classname = "crownbox";
        this.drawbox(classname, classname+playerid, this.getplayertableau(playerid));

    }

    drawcarddisplaybox(playerid){
        let classname = "carddisplaybox";
        this.drawbox(classname, classname+playerid, this.getplayertableau(playerid));
    }

    drawboards(players){
        for( let i = 0; i < players; i++){
            this.drawplayertableau(i);
        }
    }

    drawcard(playerid, card, parent, color){
        classname = "card";
        let id = classname + card + "p" + playerid;
        card = this.drawbox(classname, id, parent);
    }
}