---
title: 3.2 CMake - Тесы для библиотеки
tags:
  - cmake
---
### Тесты

##### Для написания тестов мы используем фреймворк [GTest](https://github.com/google/googletest).

Тесты хранятся в отдельной  директории:
```
. 
└── math-eigen / 
├── include 
├── src 
├── tests/                # директория с тестами (отдельный проект)
| ├── CMakeLists.txt      # CMakeLists для тестов
| ├── test1.cc            # файл с тестами
| ├── test2.cc            # файл с тестами
└── CMakeLists.txt

```

##### Рассмотрим на примере библиотеки math:

CMakeLists.txt основонго проекта:

```cmake
option(MATH_TESTS "Enable integration tests" OFF) # опция включения тестов
...
if(MATH_TESTS)
  enable_testing()
  add_subdirectory(tests) # добавление директории с тестами 
endif()
...
unset(MATH_TESTS CACHE)
...
```

CMakeLists.txt директории tests

```cmake
find_package(GTest REQUIRED) 

file(GLOB TEST_SOURCES "*.cc") # группировка всех файлов *.сс в директории

add_executable(${PROJECT_NAME}-test) # создание таргета(имя исполняемого файла)
set_target_properties(${PROJECT_NAME}-test PROPERTIES # установка стандарта
  CXX_STANDARD 20
  CXX_STANDARD_REQUIRED ON
  CXX_EXTENSIONS OFF
)

target_sources(${PROJECT_NAME}-test PRIVATE ${TEST_SOURCES}) # задание исходников

target_link_libraries(${PROJECT_NAME}-test 
  PRIVATE
  GTest::Main # библиотека gtest
  ${PROJECT_NAME} # библиотека, которую тестируем
)
# на windows частичное копирование библиотек для исполняемого файла
if(WIN32)
  add_custom_command(TARGET ${PROJECT_NAME}-test
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:${PROJECT_NAME}-test> $<TARGET_FILE_DIR:${PROJECT_NAME}-test>
    COMMAND_EXPAND_LISTS
  )

  # copy lib${PROJECT_NAME}.dll folder with ${PROJECT_NAME}-test.exe
  if(NOT "${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")
    message(STATUS "copying ${CMAKE_BINARY_DIR}/lib${PROJECT_NAME}.dll to ${CMAKE_CURRENT_BINARY_DIR}/lib${PROJECT_NAME}.dll")
    add_custom_command(TARGET ${PROJECT_NAME}-test
      POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E copy "${CMAKE_BINARY_DIR}/lib${PROJECT_NAME}.dll" "${CMAKE_CURRENT_BINARY_DIR}/lib${PROJECT_NAME}.dll"
      COMMAND_EXPAND_LISTS
    )
  endif()
endif()
```