export function saveNickname(nickname) {
    localStorage.setItem("nickname", nickname);
  }
  
  export function getNickname() {
    return localStorage.getItem("nickname") || "";
  }
  