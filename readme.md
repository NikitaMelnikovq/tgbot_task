Здравствуйте, спасибо, что уделили мне своё время!

Для разработки бота использовался python версии 3.11, все необходимые модули для работы бота можно найти в файле requirements.txt.

Таблица tasks состоит из следующих полей: айди задачи(id), айди пользователя(user_id), к которому привязана задача, заголовок задачи(title) и её описание(description).

Также есть таблица users с одним полем - user_id, это - все пользователи, использующие нашего бота.

Обращаю внимание, что user_id - это поле с типом BIGINT (поскольку не все айди пользователей телеграмм помещаются в INT)

По всем вопросам(если вдруг не запускается или что-то идёт не так, писать в телеграмм - @n1sq6).