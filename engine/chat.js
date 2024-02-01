const puppeteer = require('puppeteer');
const fs = require('fs').promises;
require('dotenv').config();

(async () => {
  // Инициализация браузера и новой страницы
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // Получаем токен
  const token = process.env.TOKEN;

  // Получаем сообщения
  const messageData = await fs.readFile('tempfiles/message.json', 'utf8');
  const message = JSON.parse(messageData).message;

  // Открытие chat.html 
  const pathToHtml = `file://${process.cwd()}/cores/chat.html`;
  await page.goto(pathToHtml);

  // Используем функцию `evaluate`, чтобы выполнить скрипт на странице
  const responses = await page.evaluate((token, message) => {
    return new Promise((resolve, reject) => {
      puter.authToken = token;
      puter.ai.chat(message).then(response => {
        resolve(response.message);
      }).catch(error => reject(error));
    });
  }, token, message);

  console.log(responses);

  // Сохраняем данные в JSON файл
  await fs.writeFile('tempfiles/response.json', JSON.stringify(responses));

  // Закрытие браузера
  await browser.close();
})();