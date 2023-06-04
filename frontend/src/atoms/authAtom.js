import { atom } from "recoil";

export const tokenState = atom({
  key: "tokenState",
  default: "", // Initial value is an empty string
});


export const loggedUserNameState = atom({
  key: "loggedUserNameState",
  default: "", // Initial value is an empty string
});


export const sessionState = atom({
  key: "sessionState",
  default: true,
});



export const uploadState = atom({
  key: "uploadState",
  default: false,
});


export const is_pushed = atom({
  key: "is_pushed",
  default: false, // Initial value is an empty string
});
