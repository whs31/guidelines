---
title: 8. C++ - Форматирование кода
tags:
  - cxx
---
### Отступы и табуляция
Как и [Google](https://google.github.io/styleguide/cppguide.html#Spaces_vs._Tabs), мы используем **2** пробела на отступ.

Секции области видимости в классах также должны иметь дополнительный отступ в 1 пробел.
Члены пространства имен также должны иметь отступ в 2 пробела.

Пример:
```cpp
namespace ns {
  class Cat {
   public:
    auto meow() -> void;
   private:
    void* data;
  };
}
```

### Clang-format
```json
---
BasedOnStyle: LLVM
AccessModifierOffset: '-1'
AlignTrailingComments: 'true'
AllowShortCaseLabelsOnASingleLine: 'true'
AllowShortFunctionsOnASingleLine: All
AllowShortIfStatementsOnASingleLine: Never
AllowShortLambdasOnASingleLine: All
AlwaysBreakAfterDefinitionReturnType: None
AlwaysBreakAfterReturnType: None
BreakBeforeBraces: Mozilla
BreakConstructorInitializers: BeforeComma
BreakInheritanceList: BeforeColon
ColumnLimit: '100'
CompactNamespaces: 'false'
ConstructorInitializerAllOnOneLineOrOnePerLine: 'false'
ConstructorInitializerIndentWidth: '2'
ContinuationIndentWidth: '2'
IndentCaseLabels: 'true'
IndentWidth: '2'
IndentWrappedFunctionNames: 'false'
Language: Cpp
NamespaceIndentation: All
PointerAlignment: Left
SortIncludes: 'false'
SortUsingDeclarations: 'false'
SpaceAfterTemplateKeyword: 'true'
SpaceBeforeCpp11BracedList: 'true'
Standard: Cpp11
UseTab: Never

...
```