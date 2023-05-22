# discord-bot
請使用python3.8以上版本  
自行將機器人TOKEN放入至.env裡  
並根據requestment.txt安裝所需套件  
即可啟動bot.py  

## /addrules
### 傳送一個embed 依照點擊的emoji增加身分組
roles 必填: 請依序填入身分組, 中間以空格分隔(預設就會有空格, 請勿調動)
title 選填: 如未輸入embed第一行會顯示 "自定義title"  
where 選填: 輸入channel ID (僅限數字), 當where沒有填入值時, 則在哪裡使用slash command就send message到哪裡, 否則message會send到指定的channel  

## /say
### 輸入想說的話, 機器人會幫你傳送到想要的頻道
echo 必填: 輸入想要說的話  
where 選填: 輸入channel ID (僅限數字), 當where沒有填入值時, 則在哪裡使用slash command就send message到哪裡, 否則message會send到指定的channel  

## /ping
### 顯示伺服器的連線延遲狀況

## /sendimg
### 傳送圖片(輸入url)
url 必填: 輸入圖片網址  
where 選填: 輸入channel ID (僅限數字), 當where沒有填入值時, 則在哪裡使用slash command就send message到哪裡, 否則message會send到指定的channel  

## /help 
### 使用說明
