const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8001/api";

export class CurioAPI {
  // Session Management
  static async createSession(topic, userEmail = "student@curio.ai") {
    try {
      const response = await fetch(`${API_BASE_URL}/session/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userEmail, // Fixed: backend expects user_id
          topic,
        }),
      });
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error?.message || "Failed to create session");
        error.code = data.error?.code;
        throw error;
      }
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
      if (!data.success) {
        const error = new Error(data.error?.message || "Failed to end session");
        error.code = data.error?.code;
        throw error;
      }
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
      if (!data.success) {
        const error = new Error(data.error?.message || "Failed to fetch session");
        error.code = data.error?.code;
        throw error;
      }
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
      if (!data.success) {
        const error = new Error(data.error?.message || "Request failed");
        error.code = data.error?.code;
        throw error;
      }
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
      if (!data.success) {
        const error = new Error(data.error?.message || "Evaluation failed");
        error.code = data.error?.code;
        throw error;
      }
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

  // Reports
  static async getReport(sessionId) {
    try {
      const response = await fetch(`${API_BASE_URL}/report/${sessionId}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      if (!data.success) {
        const error = new Error(data.error?.message || "Failed to fetch report");
        error.code = data.error?.code;
        throw error;
      }
      return data.data;
    } catch (error) {
      console.error("Error fetching report:", error);
      throw error;
    }
  }

  static async listUserReports(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}/report/list/${userId}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      if (!data.success) throw new Error(data.error?.message);
      return data.data.reports;
    } catch (error) {
      console.error("Error listing reports:", error);
      throw error;
    }
  }

  static async getLatestReports(limit = 10) {
    try {
      const response = await fetch(`${API_BASE_URL}/report/latest?limit=${limit}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      if (!data.success) throw new Error(data.error?.message);
      return data.data.reports;
    } catch (error) {
      console.error("Error fetching latest reports:", error);
      throw error;
    }
  }
}

export default CurioAPI;
