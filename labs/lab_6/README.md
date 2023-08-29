## Лабораторная работа №6. Сегментация текста
> Каждый студент выполняет все задания для собственного алфавита.

1. Подготовить текст из одной строки в Microsoft Word, пользуясь выбранным
алфавитом и теми же параметрами шрифта. Сделать скриншот и сохранить в
монохромный файл *.bmp, так чтобы вокруг строки не было белого фона.
2. Реализовать алгоритм расчёта горизонтального и вертикального профиля
изображения.
3. Реализовать алгоритм сегментации символов в строке на основе профилей с
прореживанием. В результате работы алгоритма возвращается массив с
координатами обрамляющих символы прямоугольников, упорядоченные в порядке
чтения слева направо, сверху вниз. Продемонстрировать либо вырезанные буквы,
либо нарисовать окаймляющие прямоугольники.
4. Построить профили символов выбранного алфавита.
5. *[Дополнительно можно реализовать алгоритм выделения строк из абзацев и
алгоритм выявления обрамляющего прямоугольника для текста в целом.]*

> Nota bene: Изображения символов в отчет вставлять так, чтобы фон изображения не
сливался с фоном Word (например, в рамке или инвертированном виде).

Идеи сегментации для курсива:
1. Проецировать профиль на наклонную ось.
2. Резать не только там, где профиль нулевой, а до некоторого порога в 1-2 пикселя.
3. Хитрым образом сдвинуть пиксельные строки, чтобы свести курсив к обычному
шрифту. 

### **Examples**

![](./output/combined/x1_01.png)
![](./output/combined/x1_02.png)
![](./output/combined/x1_03.png)
![](./output/combined/x1_04.png)
![](./output/combined/x1_05.png)
![](./output/combined/x1_06.png)
![](./output/combined/x1_07.png)
![](./output/combined/x1_08.png)
![](./output/combined/x1_09.png)
![](./output/combined/x1_10.png)
![](./output/combined/x1_11.png)
![](./output/combined/x1_12.png)
![](./output/combined/x1_13.png)
![](./output/combined/x1_14.png)
![](./output/combined/x1_15.png)
![](./output/combined/x1_16.png)
![](./output/combined/x1_17.png)
![](./output/combined/x1_18.png)
![](./output/combined/x1_19.png)
![](./output/combined/x1_20.png)
![](./output/combined/x1_21.png)
![](./output/combined/x1_22.png)
![](./output/combined/x1_23.png)
![](./output/combined/x1_24.png)
![](./output/combined/x1_25.png)
![](./output/combined/x1_26.png)
![](./output/combined/x1_27.png)
![](./output/combined/x2_01.png)
![](./output/combined/x2_02.png)
![](./output/combined/x2_03.png)
![](./output/combined/x2_04.png)
![](./output/combined/x2_05.png)
![](./output/combined/x2_06.png)
![](./output/combined/x2_07.png)
![](./output/combined/x2_08.png)
![](./output/combined/x2_09.png)
![](./output/combined/x2_10.png)
![](./output/combined/x2_11.png)
![](./output/combined/x2_12.png)
![](./output/combined/x2_13.png)
![](./output/combined/x2_14.png)
![](./output/combined/x2_15.png)
![](./output/combined/x2_16.png)
![](./output/combined/x2_17.png)
![](./output/combined/x2_18.png)
![](./output/combined/x2_19.png)
![](./output/combined/x2_20.png)
![](./output/combined/x2_21.png)
![](./output/combined/x2_22.png)
![](./output/combined/x2_23.png)
![](./output/combined/x2_24.png)
![](./output/combined/x2_25.png)
![](./output/combined/x2_26.png)
![](./output/combined/x2_27.png)