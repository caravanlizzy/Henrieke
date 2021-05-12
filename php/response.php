<?php

class Response{
    function __construct(){
        $this->validCard = 0;
        $this->moveComplete = 0;
        $this->gameState = "idle";
        $this->playedCards = array();
        $this->decks = array();
        $this->crowns = array();
    }
    function sendMoveComplete($complete) {
        if($complete) {
            echo "1";
        } else {
            echo "0";
        }
    }

    function sendGame($gameComplete) {
        $response = '';
        $playerIds = $gameComplete[0];
        $nicks = $gameComplete[1];
        $cards = $gameComplete[2];
        $decks = $gameComplete[3];
        $crowns = $gameComplete[4];
        for($i = 0; $i < count($playerIds); $i++) {
            $response .= $playerIds[$i] . ":" .$nicks[$i] . ":" . $cards[$i] . ":" . $decks[$i] . ":" . $crowns[$i];
            if($i< count($playerIds) - 1) {
                $response .= "-";
            }
        }
        echo $response;
        return $response;
    }

    function sendPlayerInfo($info) {
        $response = '';
        $response .= $info[0] . "_";
        $response .= $info[1];
        echo $response;
    }

    function sendRoundEnd($decksNCrowns) {
        $decks = $decksNCrowns[0];
        $crowns = $decksNCrowns[1];
        $response = '';
        for($i = 0; $i < count($crowns); $i++) {
            $response .= $crowns[$i] . ":" . $decks[$i];
            if($i < count($crowns) - 1) {
                $response .= "-";
            }
        }
        echo $response;
    }

    function sendGameState($gameState) {
        echo $gameState;
    }

    function sendPlayCard($response) {
        echo $response;
    }
}
?>