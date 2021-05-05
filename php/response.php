<?php

//response sollte zu access gehören und unabhängig von game senden
class Response{
    
    function __construct(){
        $this->validCard = 0;
        $this->moveComplete = 0;
        $this->gameState = "idle";
        $this->playedCards = array();
        $this->decks = array();
        $this->crowns = array();
    }

    function sendCards($cards) {
        $response = '';
        foreach($cards as $card) {
            $response .= $card . "_";
        }
        echo $response;
    }

    function encode() {
        $encoded = "";
        if($this->validCard){
            $encoded .= "v:1_";
        } else{
            $encoded .= "v:0_";
        }
        if($this->moveComplete){
            $encoded .= "m:1_";
        } else{
            $encoded .= "m:0_";
        }
        $encoded .= "g:" . $this->gameState . "_";
        for($i = 0; $i < count($this->playedCards); $i++) {
            $encoded .= "p" . $i . ":" . $this->playedCards[$i] . "_";
            $encoded .= "d" . $i . ":" . $this->decks[$i] . "_";
            $encoded .= "c" . $i . ":" . $this->crowns[$i] . "_";
        }
        return $encoded;
    }
}

// $r = new Response();
// print_r($r);
// function setCardValid() {
//     $this->validCard = 1;
// }
// function unsetCardValid() {
//     $this->validCard = 0;
// }

// function setMoveComplete() {
//     $this->moveComplete = 1;
// }
// function unsetMovesComplete() {
//     $this->moveComplete = 0;
// }

// function setDecks($decks) {
//     $this->decks = $decks;
// }

// function setPlayedCards($playedCards) {
//     $this->playedCards = $playedCards;
// }

// function setCrowns($crowns) {
//     $this->crowns = $crowns;
// }

// function setGameState($gameState) {
//     $this->gameState = $gameState;
// }

// function sendGameState() {
//     return;
// }

// function sendResponse($response) {
//     echo $response;
// }
?>