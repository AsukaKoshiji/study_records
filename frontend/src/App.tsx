import { useEffect, useState } from "react"
import axios from "axios"

// APIのベースURLを共通化（ポート変更や本番環境への移行を楽にするため）
const API_URL = "http://localhost:8000"

type StudyRecord = {
  id: number
  title: string
  content: string
  study_time: number
  study_date: string
  memo: string
}

type StudyGoal = {
  id: number
  goal_title: string
  target_hours: number
  deadline: string
}

function App() {
  // =====================
  // Records State
  // =====================
  const [records, setRecords] = useState<StudyRecord[]>([])

  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [studyTime, setStudyTime] = useState(0)
  const [studyDate, setStudyDate] = useState("")
  const [memo, setMemo] = useState("")

  const [editingId, setEditingId] = useState<number | null>(null)

  // =====================
  // Goals State
  // =====================
  const [goals, setGoals] = useState<StudyGoal[]>([])

  const [goalTitle, setGoalTitle] = useState("")
  const [targetTime, setTargetTime] = useState(0)
  const [deadline, setDeadline] = useState("")
  const [editingGoalId, setEditingGoalId] = useState<number | null>(null)

  // =====================
  // Progress State（バックエンドの型に合わせて安全に修正）
  // =====================
  const [progress, setProgress] = useState({
    total_study_time: 0,
    target_hours: 0,
    achievement_rate: 0
  })

  // =====================
  // Calendar State
  // =====================
  const [selectedDate, setSelectedDate] = useState("")

  // =====================
  // 初期データ取得
  // =====================
  useEffect(() => {
    fetchRecords()
    fetchGoals()
    fetchProgress()
  }, [])

  // =====================
  // Records API
  // =====================
  const fetchRecords = async () => {
    try {
      const res = await axios.get(`${API_URL}/study-records`)
      setRecords(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const createRecord = async () => {
    try {
      await axios.post(`${API_URL}/study-records`, {
        title,
        content,
        study_time: studyTime,
        study_date: studyDate,
        memo
      })

      fetchRecords()
      fetchProgress()

      setTitle("")
      setContent("")
      setStudyTime(0)
      setStudyDate("")
      setMemo("")
    } catch (err) {
      console.error(err)
    }
  }

  const updateRecord = async () => {
    try {
      await axios.put(`${API_URL}/study-records/${editingId}`, {
        title,
        content,
        study_time: studyTime,
        study_date: studyDate,
        memo
      })

      fetchRecords()
      fetchProgress()

      setEditingId(null)
      setTitle("")
      setContent("")
      setStudyTime(0)
      setStudyDate("")
      setMemo("")
    } catch (err) {
      console.error(err)
    }
  }

  const deleteRecord = async (id: number) => {
    try {
      await axios.delete(`${API_URL}/study-records/${id}`)
      fetchRecords()
      fetchProgress()
    } catch (err) {
      console.error(err)
    }
  }

  // =====================
  // Goals API
  // =====================
  const fetchGoals = async () => {
    try {
      const res = await axios.get(`${API_URL}/study-goals`)
      setGoals(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  const createGoal = async () => {
    try {
      await axios.post(`${API_URL}/study-goals`, {
        goal_title: goalTitle,
        target_hours: targetTime,
        deadline
      })

      fetchGoals()
      fetchProgress() // 目標作成時にも進捗（達成率）を再計算

      setGoalTitle("")
      setTargetTime(0)
      setDeadline("")
    } catch (err) {
      console.error(err)
    }
  }

  const updateGoal = async () => {
    try {
      await axios.put(`${API_URL}/study-goals/${editingGoalId}`, {
        goal_title: goalTitle,
        target_hours: targetTime,
        deadline
      })

      fetchGoals()
      fetchProgress() // 目標更新時にも進捗を再計算

      setEditingGoalId(null)
      setGoalTitle("")
      setTargetTime(0)
      setDeadline("")
    } catch (err) {
      console.error(err)
    }
  }

  const deleteGoal = async (id: number) => {
    try {
      await axios.delete(`${API_URL}/study-goals/${id}`)
      fetchGoals()
      fetchProgress() // 目標削除時にも進捗を再計算
    } catch (err) {
      console.error(err)
    }
  }

  // =====================
  // Progress API
  // =====================
  const fetchProgress = async () => {
    try {
      const res = await axios.get(`${API_URL}/progress`)
      setProgress(res.data)
    } catch (err) {
      console.error(err)
    }
  }

  // カレンダーフィルター
  const filteredRecords = selectedDate
    ? records.filter((r) => r.study_date === selectedDate)
    : records

  // =====================
  // UI (すべてのボタン・フォームを完全復活)
  // =====================
  return (
    <div>
      <h1>Study App</h1>

      {/* Progress */}
      <h2>Progress</h2>
      <p>合計: {progress.total_study_time} 分</p>
      {/* progress.achievement_rate がundefinedの時でも落ちないように安全に呼び出し */}
      <p>達成率: {(progress.achievement_rate ?? 0).toFixed(1)} %</p>

      <hr />

      {/* Calendar */}
      <h2>Calendar</h2>
      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
      />

      <hr />

      {/* Goals */}
      <h2>Goals</h2>

      <input
        placeholder="目標"
        value={goalTitle}
        onChange={(e) => setGoalTitle(e.target.value)}
      />

      <input
        type="number"
        placeholder="時間"
        value={targetTime}
        onChange={(e) => setTargetTime(Number(e.target.value))}
      />

      <input
        type="date"
        value={deadline}
        onChange={(e) => setDeadline(e.target.value)}
      />

      {editingGoalId ? (
        <button onClick={updateGoal}>更新</button>
      ) : (
        <button onClick={createGoal}>登録</button>
      )}

      {goals.map((g) => (
        <div key={g.id}>
          <h3>{g.goal_title}</h3>
          <p>{g.target_hours}時間</p>
          <p>{g.deadline}</p>

          <button
            onClick={() => {
              setEditingGoalId(g.id)
              setGoalTitle(g.goal_title)
              setTargetTime(g.target_hours)
              setDeadline(g.deadline)
            }}
          >
            編集
          </button>

          <button onClick={() => deleteGoal(g.id)}>
            削除
          </button>
        </div>
      ))}

      <hr />

      {/* Records */}
      <h2>Study Records</h2>

      <input
        placeholder="タイトル"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        placeholder="内容"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />

      <input
        type="number"
        value={studyTime}
        onChange={(e) => setStudyTime(Number(e.target.value))}
      />

      <input
        type="date"
        value={studyDate}
        onChange={(e) => setStudyDate(e.target.value)}
      />

      <input
        placeholder="メモ"
        value={memo}
        onChange={(e) => setMemo(e.target.value)}
      />

      {editingId ? (
        <button onClick={updateRecord}>更新</button>
      ) : (
        <button onClick={createRecord}>登録</button>
      )}

      {filteredRecords.map((r) => (
        <div key={r.id}>
          <h3>{r.title}</h3>
          <p>{r.content}</p>
          <p>{r.study_time}分</p>
          <p>{r.study_date}</p>
          <p>{r.memo}</p>

          <button
            onClick={() => {
              setEditingId(r.id)
              setTitle(r.title)
              setContent(r.content)
              setStudyTime(r.study_time)
              setStudyDate(r.study_date)
              setMemo(r.memo)
            }}
          >
            編集
          </button>

          <button onClick={() => deleteRecord(r.id)}>
            削除
          </button>
        </div>
      ))}
    </div>
  )
}

export default App