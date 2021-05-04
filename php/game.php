<?php
require 'dbconnecter.php';

class Game{
    function __construct($conn, $gameId) {
        $this->dbConnecter = new DbConnecter($conn, $gameId);
        $this->gameId = $gameId;
    }

    function createGame() {
        $this->dbConnecter->createGame();
    }

    function startGame() {
        echo "Starting Game.";
        echo "<br>";
        $this->dbConnecter->setGameState("running");
    }

    function endGame() {
        $this->dbConnecter->setGameState("idle");
        echo "Game Over!";
    }

    function deleteGame() {
        $this->dbConnecter->deleteAllPlayers();
        $this->dbConnecter->deleteMove();
        $this->dbConnecter->deleteGame();
    }

    function endRound() {
        $result = $this->getRoundResult();
        $c = $this->dbConnecter->getCrowns(4);
        $this->updateDecks($result);
        $updatedCrown = $this->updateCrowns($result);
        // print_r($updatedCrown);
        if($this->checkWin($updatedCrown)) {
            $this->endGame();
        } else{
            $this->nextRound();
        }
    }

    function nextRound() {
        $this->dbConnecter->resetMove();
        $this->dbConnecter->increaseRound();
    }

    function checkWin($updatedCrown) {
        if($updatedCrown > 1){
            return TRUE;
        }
    }

    function playCard($playerId, $card) { // main function for the game flow
        if(!$this->isCardAvailable($playerId, $card)) {
            echo "card not available";
            return;
        }
        $this->dbConnecter->setCard($playerId, $card);
        if($this->dbConnecter->checkMoveComplete()) {
            $this->endRound();
        }
    }


    function addPlayer($nick) {
        $playerId = $this->dbConnecter->createPlayer($nick);
        $this->dbConnecter->increasePlayerCount();
        $this->dbConnecter->createMove($playerId);
    }



    function isCardAvailable($playerId, $card) {
        $avCards = $this->dbConnecter->getDeck($playerId);
        if($avCards[$card] == '1') {
            return TRUE;
        }
    }


    function updateDecks($results) {
        $playerIds = $this->dbConnecter->getPlayerIds();
        for($i = 0; $i < count($playerIds); $i++) {
            $playerId = $playerIds[$i];
            $card = $this->dbConnecter->getCard($playerId);
            $result = $results[$i];
            $newDeck = $this->calcNewDeck($playerId, $card, $result);
            $this->dbConnecter->updateDeck($playerId, $newDeck);
        }
    }

    function updateCrowns($result) {
        $playerIds = $this->dbConnecter->getPlayerIds();
        for($i = 0; $i < count($result); $i++) {
            if($result[$i] == "win") {
                $playerId = $playerIds[$i];
                $newCrowns = $this->dbConnecter->addCrown($playerId);
                return $newCrowns;
            }
        }
    }

    function calcNewDeck($playerId, $card, $result) {
        $deck = $this->dbConnecter->getDeck($playerId);
        $stopIndex = $card;
        if($result == "win") {
            // echo "crown won";
            // echo "<br>";
            $stopIndex --;
        }
        for($i = 0; $i < $stopIndex; $i++) {
            $deck = $this->removeHighestCard($deck);
        }
        return $deck;
    }

    function removeHighestCard($deck) {
        for($i = 10; $i > 0; $i--) {
            if($deck[$i] == '1') {
                $deck[$i] = "0";
                return $deck;
            }
        }
        return $deck;
    }

    function getRoundResult() {
        $cards = $this->getPlayedCards();
        $highest = $this->findHighestCard($cards);
        $occurrence = $this->getCardOccurrence($cards, $highest);
        $result = $this->calcRoundResult($cards, $highest, $occurrence);
        return $result;
    }

    function calcRoundResult($cards, $highest, $occurrence) {
        $result = array_fill(0, count($cards), "loss");
        if($occurrence == 1) {
            $index = array_search($highest, $cards);
            $result[$index] = "win";
        }
        else {
            for($i = 0; $i < count($cards); $i++) {
                if($cards[$i] == $highest) {
                    $result[$i] = "tie";
                }
            }
        }
        return $result;
    }

    function findHighestCard($cards) {
        return max($cards);
    }

    function getCardOccurrence($cards, $card) {
        $occurrence = 0;
        for( $i = 0; $i < count($cards); $i++) {
            if($cards[$i] == $card) {
                $occurrence ++;
            }
        }
        return $occurrence;
    }

    function getPlayedCards() {
        $playerIds = $this->dbConnecter->getPlayerIds();
        $cards = array();
        for($i = 0; $i < count($playerIds); $i++) {
            $newCard = $this->dbConnecter->getCard($playerIds[$i]);
            array_push($cards, $newCard);
        }
        return $cards;
    }

}

?>