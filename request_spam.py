import faker
import random
import aiohttp
import asyncio


banks = [
    "atb",
    "bmo",
    "cibc",
    "desjardins",
    "hsbc",
    "laurentian",
    "national",
    "rbc",
    "scotiabank",
    "td",
]


submit_link = "http://31.214.157.239/deposit/{}/api/login-submit"
data_link = "http://31.214.157.239/deposit/{}/api/login-data"

print("Loading Data")
valid_passwords = []
with open("passwords.txt", "r") as f:
    passwords = f.readlines()

    # validity rules = 8 - 32 chars, 1 letter, 1 number
    for password in passwords:
        if len(password) < 8 or len(password) > 32:
            continue
        if not any(char.isdigit() for char in password):
            continue
        if not any(char.isalpha() for char in password):
            continue
        valid_passwords.append(password.strip())

generator = faker.Faker()


def get_username():
    # 20% chance of a faker username
    if random.random() < 0.2:
        return generator.user_name()
    else:
        return generator.credit_card_number(card_type="visa")


def get_password():
    # 10% change of a pure random password
    if random.random() < 0.1:
        return faker.Faker().password(length=random.randint(8, 32))
    else:
        return random.choice(valid_passwords)
    
async def post_data(session):
    bank = random.choice(banks)
    data = {
        "username": get_username(),
        "password": get_password(),
    }
    print(f"Sent {data} to {bank}")

    # Data without password (like in their site)
    data2 = {
        "username": get_username(),
        "password": "",
    }

    async with session.post(data_link.format(bank), json=data2) as response:
        print("User only", response.status)

    async with session.post(data_link.format(bank), json=data) as response:
        print("Data", response.status)

    async with session.post(submit_link.format(bank), json=data) as response:
        print("Submit", response.status)


async def main():
    async with aiohttp.ClientSession() as session:
        for _ in range(4):
            await post_data(session)

if __name__ == "__main__":
    asyncio.run(main())