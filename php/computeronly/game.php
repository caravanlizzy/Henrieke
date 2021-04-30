<?php

require 'player.php';

class Game{
    function __construct() {
        $this->players = [];
        $this->crownsToWin = 2;
        $this->round = 0;
        $this->verbose = true;
    }

    function addPlayer($name, $strategy = "randomBot") {
        $player = new Player($name, $this, $strategy);
        array_push($this->players, $player);
    }

    function reset() {
        $this->round = 0;
    }

    function printRoundResults($roundResults, $playedCards) {
        for($i = 0; $i < count($this->players); $i++) {
            print_r($this->players[$i]->name);
            echo " played :";
            print_r($playedCards[$i]);
            echo "<br>";
        }
        echo "<br>";
    }

    function updatePlayers($roundResults, $playedCards) {
        for($i = 0; $i < count($roundResults); $i++) {
            $roundResult = $roundResults[$i];
            $cards; // number of cards to remove at the end of the round
            if($roundResult == "win") {
                $this->updateWinner($i, $playedCards);
            } else if($roundResult == "loss") {
                $this->updateLoser($i, $playedCards);
            } else{
                $this->updateTier($i, $playedCards);
            }
        }
        if ($this->verbose) {
            $this->printRoundResults($roundResults, $playedCards);
        }
    }

    function updateWinner($playerIndex, $playedCards) {
        $cards = $playedCards[$playerIndex] - 1;
        $this->players[$playerIndex]->crowns += 1;
        $this->players[$playerIndex]->removeHighestCards($cards);
    }

    function updateLoser($playerIndex, $playedCards) {
        $cards = $playedCards[$playerIndex];
        $this->players[$playerIndex]->removeHighestCards($cards);  
    }

    function updateTier($playerIndex, $playedCards) {
        $card = $playedCards[$playerIndex];
        $this->players[$playerIndex]->removecard($card);
    }

    function checkOver() {
        for($i = 0; $i < count($this->players); $i++) {
            $player = $this->players[$i];
            if($player->crowns >= $this->crownsToWin) {
                return true;
            }
        }
        if($this->round > 25) {
            return true;
        }
        return false;
    }

    function start() {
        $this->prepareGame();
        print("Welcome to Henriekow! Good luck.\r\n <br>");
        $gameOver = $this->checkOver();
        while ($gameOver == false){
            $this->runRound();
            $gameOver = $this->checkOver();
        }
        if($this->findWinner() == false) {
            echo "Game is tied.";
        }
        else{
            print_r($this->findWinner()->name);
            echo " wins the game!";
        }
    }

    function prepareGame() {
        $this->reset();
        $this->setWinCondition();
    }

    function setWinCondition() {
        $nPlayers = count($this->players);
        if($nPlayers < 2){
            echo "Not enough players \r\n";
        } else if( $nPlayers == 2) {
            $this->crownsToWin = 3;
        } else{
            $this->crownsToWin = 2;
        }
    }

    function runRound() {
        $playedCards = $this->getPlayedCards();
        $roundResults = $this->getroundResults($playedCards);
        $this->updatePlayers($roundResults, $playedCards);
        $this->round += 1;
    }

    function getPlayedCards() {
        $playedCards = [];
        foreach($this->players as $player) {
            array_push($playedCards, $player->playcard());
        }
        return $playedCards;
    }

    function getroundResults($playedCards) {
        $roundResults = [];
        foreach($playedCards as $p) {
            array_push($roundResults, "loss");
        }
        $highestCard = max($playedCards);
        $occurence = array_count_values($playedCards)[$highestCard];
        if($occurence == 1) {
            $index = array_search($highestCard, $playedCards);
            $roundResults[$index] = "win";
        } else {
            for($i = 0; $i < count($roundResults); $i++) {
                if($playedCards[$i] == $highestCard) {
                    $roundResults[$i] = "tie";
                }
            }
        }
        return $roundResults;
    }

    function findWinner() {
        foreach($this->players as $player) {
            if($player->crowns >= $this->crownsToWin) {
                return $player;
            }
        }
        return false;
    }
}



?>