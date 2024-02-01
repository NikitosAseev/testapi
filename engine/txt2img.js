const puppeteer = require('puppeteer');
const fs = require('fs').promises;
require('dotenv').config();

(async () => {
  try {
    // Инициализация браузера и новой страницы
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Получаем токен
    const token = process.env.TOKEN;

    // Получаем сообщения 
    const messageData = await fs.readFile('tempfiles/message.json', 'utf8');
    const message = JSON.parse(messageData).message;

    // Открытие txt2img.html
    const pathToHtml = `file://${process.cwd()}/cores/txt2img.html`;
    await page.goto(pathToHtml);

    // Используем функцию evaluate, чтобы выполнить скрипт на странице
    await page.evaluate((token, message) => {
      return new Promise((resolve, reject) => {
        puter.authToken = token;
        puter.ai.txt2img(message, true).then(image => {
          resolve(image);
        }).catch(error => reject(error));
      });
    }, token, message);

    // Ожидание появления изображения
    await page.waitForSelector('img');

    // Получение и сохранение изображения
    const imgSrc = await page.$eval('img', (img) => img.src);
    const base64Data = imgSrc.replace(/^data:image\/png;base64,/, '');
    await fs.writeFile('image.png', base64Data, 'base64');

    // Закрытие браузера
    await browser.close();

    console.log('Изображение успешно сохранено.');
  } catch (error) {
    console.error('Произошла ошибка:', error);
  }
})();