---
title: 3.1 CMake - Исполняемый файл библиотеки
tags:
  - cmake
---
### Создание исполняемого файла библиотеки для тестирования или какого-либо еще применения.

CMakeLists.txt  основного проекта(библиотеки).
`рассмотрим на примере библиотеки с именем math`

> [!error] Замечание
> При копировании заменить все вхождения math на имя своей библиотеки

```cmake
...
# создание опции для исполняемого файла 
option(MATH_STANDALONE "Build dev executable (testing only)" OFF)
...
# подключение сабдиректории с отдельным CMakeLists.txt для отдельного исполняемого таргета 
if(MATH_STANDALONE)
    message(STATUS "[MATH] building test executable for developers")
    add_subdirectory(bin)
endif()
...
unset(MATH_STANDALONE CACHE)
```

CMakeLists.txt в директории bin 
```cmake
# создание нового таргета
add_executable(${PROJECT_NAME}-bench)
# добавление необходимых файлов в прроект (так же могут быть *.qrc если это qml приложение)
target_sources(${PROJECT_NAME}-bench
        PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/main.cc
)
# подключение нашего основного проекта как библиотеки
target_link_libraries(${PROJECT_NAME}-bench PUBLIC ${PROJECT_NAME} )
```

Для сборки в standalone, необходимо извне передать опцию cmake. 
Опция cmake: `-DMATH_STANDALONE=ON`
Пример сборки из консоли
```bash
cmake -S . -B target/debug -G Ninja -DMATH_STANDALONE=ON
```
Аналогичным образом это выстовляется в конфигурации проекта в вашей Ide(Clion/QtCreator) в поле `CMake options`:
```
-DMATH_STANDALONE=ON
```
