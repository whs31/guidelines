---
title: 2. C++ - Используемый стандарт
tags:
  - cxx
---
# Используемый стандарт С++, компилятор и расширения

### Стандарт C++
На данный момент основным используемым стандартом является **C++20** с незначительными отсутствующими частями стандартной библиотеки.

> Для разработчиков под *Astra Linux SE 1.6* максимально высоким стандартом является **C++14** без расширений.

Не допускается использование следующих заголовочных файлов стандартной библиотеки:
- `format` - вместо `std::format` рекомендуется использовать `fmt::format` из библиотеки `fmt` (доступна в [нашем репозитории](http://uav.radar-mms.com/ui/packages/conan:%2F%2Ffmt?projectKey=radar))
- `source_location` - вместо `std::source_location` рекомендуется использовать библиотеку `Boost`.

Модули из С++20 в данный момент не поддерживаются используемой версией *CMake*, поэтому их использование также запрещено (в т.ч. замена директивы `#include` на ключевое слово `import`)

### Компилятор 
Основным используемым компилятором является **GCC 10.2.0**. В роли резервного компилятора выступает **Clang 15**.

Правильно написанная библиотека/приложение должно компилироваться **всеми основными компиляторами** (*GCC* → *Clang* → *MSVC* в порядке убывания приоритета)

### Нестандартные расширения компилятора
#### Атрибуты GCC
Атрибуты (ключевое слово `__attribute__`) находятся под запретом, так как не поддерживаются компиляторами, отличными от GCC.

##### Как заменить `__attribute__((constuctor))`?

Этот атрибут обычно используется для автоматического вызова какой-либо свободной функции **при линковке**.
###### Неправильный код
```cpp 
auto __attribute__((constructor)) print_version() -> void {
	fmt::print("loaded library {} version {}.{}", 
		PROJECT_NAME, 
		PROJECT_VERSION_MAJOR,
		PROJECT_VERSION_MINOR
	);
}
```
Данный код не будет скомпилирован компиляторами MSVC и, потенциально, Clang.

###### Правильный код
```cpp
struct constructor {
	explicit constructor(void (*f)(void)) { f(); }
};

static auto print_version = constructor(+[]() -> void {
	fmt::print("loaded library {} version {}.{}", 
		PROJECT_NAME, 
		PROJECT_VERSION_MAJOR,
		PROJECT_VERSION_MINOR
	);
});
```
Семантический смысл остается тем же, но этот вариант скомпилируется любым из современных компиляторов С++. 
Если вам требуется вызывать `constructor` часто, то `struct constructor` можно параметризировать через шаблон.

##### Как заменить `__attribute__((packed))`?
Этот атрибут используется для того, чтобы убрать паддинг (отступ) между членами внутри структуры.
###### Неправильный код
```cpp
struct Data 
{
	int a;
	bool b;
	float c;
	long long d;
} __attribute__((packed));
```
###### Правильный код
```cpp
#pragma pack(push, 1)
struct [[gnu::packed]] Data 
{
	int a;
	bool b;
	float c;
	long long d;
};
#pragma pack(pop)
```

#### Встроенные функции компиляторов (*интринсики*)
Если интринсик предоставляет функционал, который помогает компилятору в оптимизации кода, или же необходим для корректной работы программы (напр. `__declspec`), то его использование должно быть абстрагировано с помощью макроса или функции.

В остальных случаях интринсики ведут к нарушениям кроссплатформенности программы и их использование осуждается.

##### Если необходимо использование интринсика
Например, для явного указания, что та или иная ветвь потока управления в коде никогда не будет выполнена, существует интринсик *GCC* `__builtin_unreachable`.
###### Неправильный код
```cpp
bool a = false;
switch(static_cast<char>(a)) {
	case 0: /* ... */ break;
	case 1: /* ... */ break;
	default: __builtin_unreachable();
}
```

###### Правильный код
```cpp
[[noreturn]] auto unreachable() -> void {
	#if defined(_MSC_VER) &&!defined(__clang__) // MSVC
	__assume(false);
	#else 
	__builtin_unreachable();
	#endif
}

bool a = false;
switch(static_cast<char>(a)) {
	case 0: /* ... */ break;
	case 1: /* ... */ break;
	default: ::unreachable();
}
```

##### Если интринсик нужен для импорта/экспорта в динамической библиотеке
Для того, чтобы символы корректно линковались в динамических библиотеках, их необходимо помечать как экпортируемые. Для этого используется комбинация `__declspec(dllexport)`/`__declspec(dllimport)`.

Пример корректного кода для публичного заголовочного файла в библиотеке:
`global.h`
```cpp
#if defined(_WIN32)
# if defined(TEST_LIBRARY)
#  define TEST_EXPORT __declspec(dllexport)
# elif defined(TEST_STATIC_LIBRARY)
#  define TEST_EXPORT
# else
#  define TEST_EXPORT __declspec(dllimport)
# endif
#else
# define TEST_EXPORT
#endif
```

`test.h`
```cpp
#include <global.h>

TEST_EXPORT auto meow() -> void;

class TEST_EXPORT Cat { /* ... */ };
struct TEST_EXPORT Dog { /* ... */ };
```

#### Особые директивы препроцессора
Нестандартные директивы препроцессора запрещены к использованию. В их число входит:
- `#pragma` - в т.ч. `#pragma omp`, `pragma region` и т. д.
- `#elifdef`
- `#include_next`

> [!important] Замечание
> Директива `#pragma once` разрешена и поощряется, так как поддерживается любым современным компилятором и является полностью кроссплатформенной.

#### Прочие нестандартные расширения языка
Также **запрещены:**
- Ассемблерные вставки
- Макросы `__COUNTER__`, `__PRETTY_FUNCTION__`
- *Elvis-operator* (`?:`): [Wikipedia](https://en.wikipedia.org/wiki/Elvis_operator)

#### Далее: [[headers|Заголовочные файлы]]