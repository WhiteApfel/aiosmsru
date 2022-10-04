# 🚧 aioSMSru

- [x] Send SMS
- [x] Check SMS status
- [x] Get SMS cost
- [x] Get balance
- [x] Get limit
- [x] Get free limit
- [x] Get my senders
- [x] Check api_id or login and password
- [ ] Add to stoplist
- [ ] Remove from stoplist
- [x] Get stoplist
- [ ] Add callback
- [ ] Remove callback
- [ ] Get callbacks
- [x] Callcheck

## 🧑‍💻 How to use

I gave an example for an async client, but sync is no different, 
you just don't need to use await. Get satisfaction 😌

```python
from smsru import AioSMSru, SMSru

client = AioSMSru("app_id")

async def main():
    print(await client.sms_cost("79991398805", "I'm in serious shit"))
    
    # 79991398805 and 79956896018 <- I feel totally lost
    scend = await client.send_sms(
        recipients=['79991398805', '79956896018'],
        messages="I feel totally lost"
    )
    print(await client.check_sms([m_id for m_id in sensed.sms.keys()]))
    
    # 79991398805 <- If i'm asking for help
    # 79956896018 <- it's only because
    scend = await client.send_sms(
        recipients=['79991398805', '79956896018'],
        messages=["If i'm asking for help", "it's only because"]
    )
    
    call = await client.callcheck('79991398805')
    print(call.code == input("Last 4 digits of incoming call number: "))
```