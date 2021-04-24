class Graphic{
    constructor(){
        this.playertableaus = [];
    }

    drawmainframe(){
        let frame = document.createElement("div");
        frame.className = "mainframe";
        frame.id = "mainframe";
        document.body.append(frame);
    }

    drawplayertableau(playerid){
        let tableau = document.createElement("div");
        tableau.className = "playerframe";
        document.getElementById("mainframe").append(tableau);
        this.playertableaus.push(tableau);
    }


}