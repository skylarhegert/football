import streamlit as st

import { useState } from 'react'
import { Button } from "/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "/components/ui/card"
import { Input } from "/components/ui/input"
import { Label } from "/components/ui/label"
import { Textarea } from "/components/ui/textarea"
import { Star } from "lucide-react"
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "/components/ui/dialog"
import { Plus } from "lucide-react"

export default function AmericanFootballPredictor() {
  const [teamAStats, setTeamAStats] = useState({
    touchdowns: '',
    yards: '',
    interceptions: '',
    sacks: '',
  })
  const [teamBStats, setTeamBStats] = useState({
    touchdowns: '',
    yards: '',
    interceptions: '',
    sacks: '',
  })
  const [historicalData, setHistoricalData] = useState({
    previousEncounters: '',
    homeAwayPerformance: '',
  })
  const [teamAPlayers, setTeamAPlayers] = useState<{ name: string; touchdowns: string; yards: string }[]>([])
  const [teamBPlayers, setTeamBPlayers] = useState<{ name: string; touchdowns: string; yards: string }[]>([])
  const [prediction, setPrediction] = useState<string | null>(null)
  const [feedback, setFeedback] = useState({
    comment: '',
    rating: 0,
  })
  const [isTeamAPlayerModalOpen, setTeamAPlayerModalOpen] = useState(false)
  const [isTeamBPlayerModalOpen, setTeamBPlayerModalOpen] = useState(false)
  const [newPlayer, setNewPlayer] = useState({ name: '', touchdowns: '', yards: '' })

  const handleTeamAChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setTeamAStats({ ...teamAStats, [name]: value })
  }

  const handleTeamBChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setTeamBStats({ ...teamBStats, [name]: value })
  }

  const handleHistoricalDataChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setHistoricalData({ ...historicalData, [name]: value })
  }

  const handleFeedbackChange = (e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
    const { name, value } = e.target
    setFeedback({ ...feedback, [name]: value })
  }

  const handleNewPlayerChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setNewPlayer({ ...newPlayer, [name]: value })
  }

  const addTeamAPlayer = () => {
    setTeamAPlayers([...teamAPlayers, newPlayer])
    setNewPlayer({ name: '', touchdowns: '', yards: '' })
    setTeamAPlayerModalOpen(false)
  }

  const addTeamBPlayer = () => {
    setTeamBPlayers([...teamBPlayers, newPlayer])
    setNewPlayer({ name: '', touchdowns: '', yards: '' })
    setTeamBPlayerModalOpen(false)
  }

  const predict = () => {
    const teamAOffense = parseFloat(teamAStats.touchdowns) + parseFloat(teamAStats.yards) / 100 - parseFloat(teamAStats.interceptions)
    const teamADefense = parseFloat(teamAStats.sacks)
    const teamBOffense = parseFloat(teamBStats.touchdowns) + parseFloat(teamBStats.yards) / 100 - parseFloat(teamBStats.interceptions)
    const teamBDefense = parseFloat(teamBStats.sacks)

    const teamAPlayerScore = teamAPlayers.reduce((acc, player) => acc + parseFloat(player.touchdowns) + parseFloat(player.yards) / 100, 0)
    const teamBPlayerScore = teamBPlayers.reduce((acc, player) => acc + parseFloat(player.touchdowns) + parseFloat(player.yards) / 100, 0)

    const teamAScore = teamAOffense - teamBDefense + teamAPlayerScore
    const teamBScore = teamBOffense - teamADefense + teamBPlayerScore

    if (teamAScore > teamBScore) {
      setPrediction(`Team A is predicted to win with a score of ${Math.round(teamAScore)} - ${Math.round(teamBScore)}`)
    } else if (teamBScore > teamAScore) {
      setPrediction(`Team B is predicted to win with a score of ${Math.round(teamBScore)} - ${Math.round(teamAScore)}`)
    } else {
      setPrediction(`The match is predicted to end in a draw with a score of ${Math.round(teamAScore)} - ${Math.round(teamBScore)}`)
    }
  }

  const submitFeedback = () => {
    localStorage.setItem('feedback', JSON.stringify(feedback))
    alert('Feedback submitted!')
    setFeedback({ comment: '', rating: 0 })
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white p-4">
      <Card className="w-full max-w-3xl">
        <CardHeader>
          <CardTitle>American Football Match Predictor</CardTitle>
          <CardDescription>Input team statistics to get a prediction for the match outcome.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <CardTitle>Team A Statistics</CardTitle>
              <div className="mb-2">
                <Label htmlFor="teamA-touchdowns">Touchdowns</Label>
                <Input id="teamA-touchdowns" name="touchdowns" value={teamAStats.touchdowns} onChange={handleTeamAChange} />
              </div>
              <div className="mb-2">
                <Label htmlFor="teamA-yards">Yards</Label>
                <Input id="teamA-yards" name="yards" value={teamAStats.yards} onChange={handleTeamAChange} />
              </div>
              <div className="mb-2">
                <Label htmlFor="teamA-interceptions">Interceptions</Label>
                <Input id="teamA-interceptions" name="interceptions" value={teamAStats.interceptions} onChange={handleTeamAChange} />
              </div>
              <div className="mb-2">
                <Label htmlFor="teamA-sacks">Sacks</Label>
                <Input id="teamA-sacks" name="sacks" value={teamAStats.sacks} onChange={handleTeamAChange} />
              </div>
              <div className="mb-2">
                <Dialog open={isTeamAPlayerModalOpen} onOpenChange={setTeamAPlayerModalOpen}>
                  <DialogTrigger asChild>
                    <Button variant="outline">
                      <Plus className="mr-2" />
                      Add Player
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                      <DialogTitle>Add Team A Player</DialogTitle>
                      <DialogDescription>Enter player statistics.</DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="player-name" className="text-right">
                          Name
                        </Label>
                        <Input id="player-name" name="name" value={newPlayer.name} onChange={handleNewPlayerChange} className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="player-touchdowns" className="text-right">
                          Touchdowns
                        </Label>
                        <Input id="player-touchdowns" name="touchdowns" value={newPlayer.touchdowns} onChange={handleNewPlayerChange} className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="player-yards" className="text-right">
                          Yards
                        </Label>
                        <Input id="player-yards" name="yards" value={newPlayer.yards} onChange={handleNewPlayerChange} className="col-span-3" />
                      </div>
                    </div>
                    <DialogFooter>
                      <Button onClick={addTeamAPlayer}>Add Player</Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>
              <div className="mb-2">
                <CardTitle>Team A Players</CardTitle>
                {teamAPlayers.map((player, index) => (
                  <div key={index} className="flex items-center justify-between mb-2">
                    <div>
                      <p className="font-semibold">{player.name}</p>
                      <p>Touchdowns: {player.touchdowns}, Yards: {player.yards}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <CardTitle>Team B Statistics</CardTitle>
              <div className="mb-2">
                <Label htmlFor="teamB-touchdowns">Touchdowns</Label>
                <Input id="teamB-touchdowns" name="touchdowns" value={teamBStats.touchdowns} onChange={handleTeamBChange} />
              </div>
              <div className="mb-2">
                <Label htmlFor="teamB-yards">Yards</Label>
                <Input id="teamB-yards" name="yards" value={teamBStats.yards} onChange={handleTeamBChange} />
              </div>
              <div className="mb-2">
                <Label htmlFor="teamB-interceptions">Interceptions</Label>
                <Input id="teamB-interceptions" name="interceptions" value={teamBStats.interceptions} onChange={handleTeamBChange} />
              </div>
              <div className="mb-2">
                <Label htmlFor="teamB-sacks">Sacks</Label>
                <Input id="teamB-sacks" name="sacks" value={teamBStats.sacks} onChange={handleTeamBChange} />
              </div>
              <div className="mb-2">
                <Dialog open={isTeamBPlayerModalOpen} onOpenChange={setTeamBPlayerModalOpen}>
                  <DialogTrigger asChild>
                    <Button variant="outline">
                      <Plus className="mr-2" />
                      Add Player
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="sm:max-w-[425px]">
                    <DialogHeader>
                      <DialogTitle>Add Team B Player</DialogTitle>
                      <DialogDescription>Enter player statistics.</DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="player-name" className="text-right">
                          Name
                        </Label>
                        <Input id="player-name" name="name" value={newPlayer.name} onChange={handleNewPlayerChange} className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="player-touchdowns" className="text-right">
                          Touchdowns
                        </Label>
                        <Input id="player-touchdowns" name="touchdowns" value={newPlayer.touchdowns} onChange={handleNewPlayerChange} className="col-span-3" />
                      </div>
                      <div className="grid grid-cols-4 items-center gap-4">
                        <Label htmlFor="player-yards" className="text-right">
                          Yards
                        </Label>
                        <Input id="player-yards" name="yards" value={newPlayer.yards} onChange={handleNewPlayerChange} className="col-span-3" />
                      </div>
                    </div>
                    <DialogFooter>
                      <Button onClick={addTeamBPlayer}>Add Player</Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              </div>
              <div className="mb-2">
                <CardTitle>Team B Players</CardTitle>
                {teamBPlayers.map((player, index) => (
                  <div key={index} className="flex items-center justify-between mb-2">
                    <div>
                      <p className="font-semibold">{player.name}</p>
                      <p>Touchdowns: {player.touchdowns}, Yards: {player.yards}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <div className="mb-4">
            <CardTitle>Historical Data</CardTitle>
            <div className="mb-2">
              <Label htmlFor="previousEncounters">Previous Encounters</Label>
              <Input id="previousEncounters" name="previousEncounters" value={historicalData.previousEncounters} onChange={handleHistoricalDataChange} />
            </div>
            <div className="mb-2">
              <Label htmlFor="homeAwayPerformance">Home/Away Performance</Label>
              <Input id="homeAwayPerformance" name="homeAwayPerformance" value={historicalData.homeAwayPerformance} onChange={handleHistoricalDataChange} />
            </div>
          </div>
          <Button onClick={predict}>Predict</Button>
        </CardContent>
        {prediction && (
          <CardFooter>
            <CardTitle>Prediction</CardTitle>
            <p>{prediction}</p>
          </CardFooter>
        )}
      </Card>
      <Card className="w-full max-w-3xl mt-4">
        <CardHeader>
          <CardTitle>User Feedback</CardTitle>
          <CardDescription>Provide feedback on the prediction accuracy.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-2">
            <Label htmlFor="feedback-comment">Comment</Label>
            <Textarea id="feedback-comment" name="comment" value={feedback.comment} onChange={handleFeedbackChange} />
          </div>
          <div className="mb-2">
            <Label htmlFor="feedback-rating">Rating</Label>
            <div className="flex items-center space-x-2">
              {[1, 2, 3, 4, 5].map((star) => (
                <Star
                  key={star}
                  className={`cursor-pointer ${star <= feedback.rating ? 'text-yellow-400' : 'text-gray-300'}`}
                  onClick={() => setFeedback({ ...feedback, rating: star })}
                />
              ))}
            </div>
          </div>
          <Button onClick={submitFeedback}>Submit Feedback</Button>
        </CardContent>
      </Card>
    </div>
  )
}
