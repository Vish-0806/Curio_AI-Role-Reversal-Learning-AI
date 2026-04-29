const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export class CurioAPI {
  // Session Management
  static async createSession(topic, userEmail = "student@curio.ai") {
    try {
      const response = await fetch(`${API_BASE_URL}/session`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_email: userEmail,
          topic,
        }),
      });
      const data = await response.json();
      if (!data.success) throw new Error(data.error?.message);
      return data.data;
    } catch (error) {
      console.error("Error creating session:", error);
      throw error;
    }
  }

  static async endSession(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/session/${sessionId}/end`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      if (!data.success) throw new Error(data.error?.message);
      return data.data;
    } catch (error) {
      console.error("Error ending session:", error);
      throw error;
    }
  }

  static async getSession(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/session/${sessionId}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      if (!data.success) throw new Error(data.error?.message);
      return data.data;
    } catch (error) {
      console.error("Error fetching session:", error);
      throw error;
    }
  }

  // Chat
  static async sendMessage(sessionId, userMessage, mode = "teach", context = null) {
    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          user_message: userMessage,
          mode,
          context,
        }),
      });
      const data = await response.json();
      if (!data.success) throw new Error(data.error?.message);
      return data.data;
    } catch (error) {
      console.error("Error sending message:", error);
      throw error;
    }
  }

  // Evaluation
  static async evaluateSession(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId }),
      });
      const data = await response.json();
      if (!data.success) throw new Error(data.error?.message);
      return data.data;
    } catch (error) {
      console.error("Error evaluating session:", error);
      throw error;
    }
  }

  // Rescue/Hints
  static async getHint(sessionId, hintLevel = 1) {
    try {
      // For now, this is a local implementation
      // In a real scenario, this would call backend
      const hints = [
        "Try breaking down the concept into smaller parts. What are the key components?",
        "Think about how this concept relates to things you already know.",
        "What would happen if you applied this concept in real life? Can you think of an example?",
      ];
      return { hint: hints[hintLevel - 1] || hints[0] };
    } catch (error) {
      console.error("Error getting hint:", error);
      throw error;
    }
  }

  // Report
  static async getReport(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/report/${sessionId}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      if (!data.success) throw new Error(data.error?.message);
      return data.data;
    } catch (error) {
      console.error("Error fetching report:", error);
      throw error;
    }
  }
}

export default CurioAPI;
