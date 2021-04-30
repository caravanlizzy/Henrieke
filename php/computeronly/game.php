<?php

require 'player.php';

class Game{
    function __construct() {
        $this->players = [];
        $this->crownstowin = 2;
        $this->round = 0;
        $this->verbose = true;
    }

    function addplayer($name, $human = false) {
        $player = new Player($name);
        if($human) {
            $player->stratergy = "human";
        }
        array_push($this->players, $player);
    }

    function reset() {
        $this->round = 0;
    }

    function printroundresults($roundresults, $playedcards) {
        for($i = 0; $i < count($this->players); $i++) {
            print_r($this->players[$i]->name);
            echo " played :";
            print_r($playedcards[$i]);
            echo "<br>";
        }
        echo "<br>";
    }

    function updateplayers($roundresults, $playedcards) {
        for($i = 0; $i < count($roundresults); $i++) {
            $roundresult = $roundresults[$i];
            $cards; // number of cards to remove at the end of the round
            if($roundresult == "win") {
                $cards = $playedcards[$i] - 1;
                $this->players[$i]->crowns += 1;
                $this->players[$i]->removehighestcards($cards);
            } else if($roundresult == "loss") {
                $cards = $playedcards[$i];
                $this->players[$i]->removehighestcards($cards);
            } else{
                $playedcard = $playedcards[$i];
                $this->players[$i]->removecard($playedcard);
            }
        }
        if ($this->verbose) {
            $this->printroundresults($roundresults, $playedcards);
        }
    }

    function checkwin() {
        for($i = 0; $i < count($this->players); $i++) {
            $player = $this->players[$i];
            if($player->crowns >= $this->crownstowin) {
                return true;
            }
        }
        return false;
    }

    function startgame() {
        $this->reset();
        $nplayers = count($this->players);
        if($nplayers < 2){
            echo "Not enough players \r\n";
        } else if( $nplayers == 2) {
            $this->crownstowin = 3;
        } else{
            $this->crownstowin = 2;
        }
        print("Welcome to Henriekow! Good luck.\r\n <br>");
        $gameover = $this->checkwin();
        while ($gameover == false){
            $this->runround();
            $gameover = $this->checkwin();
        }
        print_r($this->findwinner()->name);
        echo " wins the game!";
    }

    function runround() {
        $this->round += 1;
        $playedcards = [];
        foreach($this->players as $player) {
            array_push($playedcards, $player->playcard());
        }
        $roundresults = $this->getroundresults($playedcards);
        $this->updateplayers($roundresults, $playedcards);
    }

    function getroundresults($playedcards) {
        $roundresults = [];
        foreach($playedcards as $p) {
            array_push($roundresults, "loss");
        }
        $highestcard = max($playedcards);
        $occurence = array_count_values($playedcards)[$highestcard];
        if($occurence == 1) {
            $index = array_search($highestcard, $playedcards);
            $roundresults[$index] = "win";
        } else {
            for($i = 0; $i < count($roundresults); $i++) {
                if($playedcards[$i] == $highestcard) {
                    $roundresults[$i] = "tie";
                }
            }
        }
        return $roundresults;
    }

    function findwinner() {
        foreach($this->players as $player) {
            if($player->crowns >= $this->crownstowin) {
                return $player;
            }
        }
    }
}



?>