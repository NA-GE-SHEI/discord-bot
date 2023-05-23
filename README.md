# discord-bot
請使用python3.8以上版本  
自行將機器人TOKEN放入至.env裡

## 指令
### /say
echo 必填: 輸入想要說的話  
where 選填: 輸入channel ID (僅限數字), 當where沒有填入值時, 則在哪裡使用slash command就send message到哪裡, 否則message會send到指定的channel  

## /gpa
scope 必填: 依序輸入對應的GPA分數, 中間以", "間隔  
credit 必填: 依序輸入對應的學分數, 中間以", "間隔  

## /alarm
mm 必填: 月份  
dd 必填: 日期  
time 必填: 時間, 格式為H:M  
desc 必填: 內容  
who 選填: 輸入要提醒的人 @test  

## /keyword
顯示敏感字詞  

## /addkey
content 必填: 依序輸入要禁止的關鍵字, 中間以", "間隔  

## /rmkey
content 必填: 依序輸入要移除的關鍵字, 中間以", "間隔 

## /nick
**此command無法編輯比機器人權限還低或相同的人**  
member 必填: @使用者  
nick 必填: 輸入nickname  
