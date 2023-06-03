import { atom } from "recoil";

export const tokenState = atom({
  key: "tokenState",
  default: "", // Initial value is an empty string
});

export const is_pushed = atom({
  key: "is_pushed",
  default: false, // Initial value is an empty string
});
