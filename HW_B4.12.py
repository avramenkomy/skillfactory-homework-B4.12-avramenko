"""disclaimer:
Во избежание недоразумений, разночтений и т.д. весь код написан в одном файле. Для работы требуется данная программка + БД. 
Функция валидации введенных данных не реализована, но и по заданию это не требуется, поэтому я напишу ее когда будет время, 
поэтому важно вводить значения корректно сразу.
БД должна располагаться в той же директории, что и файл с кодом. Если БД будет располагаться в другой директории, то необходимо
скорректировать строку подключения, записанную в перменную DB_PATH строка №16"""

#Блок импорта
import uuid, datetime
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Введем константу для соединения с БД
DB_PATH = "sqlite:///sochi_athletes.sqlite3"

#Создадим базовый класс моделей таблиц
Base = declarative_base()

#Создадим модель таблицы всех атлетов
class Athelete(Base):
	""""""
	__tablename__ = "athelete"
	id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
	age = sa.Column(sa.INTEGER)
	birthdate = sa.Column(sa.TEXT)
	gender = sa.Column(sa.TEXT)
	height = sa.Column(sa.REAL)
	name = sa.Column(sa.TEXT)
	weight = sa.Column(sa.INTEGER)
	gold_medals = sa.Column(sa.INTEGER)
	silver_medals = sa.Column(sa.INTEGER)
	bronze_medals = sa.Column(sa.INTEGER)
	total_medals = sa.Column(sa.INTEGER)
	sport = sa.Column(sa.TEXT)
	country = sa.Column(sa.TEXT)


#Создадим модель таблицы User
class User(Base):
	"""Создает структуру таблицы user для хранения регистрационных данных пользователей"""
	__tablename__ = "user" #Задаем имя таблицы
	id = sa.Column(sa.INTEGER, primary_key=True, autoincrement=True)
	first_name = sa.Column(sa.TEXT)
	last_name = sa.Column(sa.TEXT)
	gender = sa.Column(sa.TEXT)
	email = sa.Column(sa.TEXT)
	birthdate = sa.Column(sa.TEXT)
	height = sa.Column(sa.REAL)

def connect_db():
	"""Устанавливает связь с БД, создает таблицы если их нет, возвращает объект сессии"""
	engine = sa.create_engine(DB_PATH) #Создаем соединение с БД
	Base.metadata.create_all(engine) #Создаем описание таблицы
	session = sessionmaker(engine) #Создаем фабрику сессий
	#Возвращем объект сессии
	return session()

#Создадим функцию запроса данных у пользователя, которая так же будет сохранять данные в таблицу
def request_data():
	"""Запрашивает данные у пользователя, конструирует объект модели User, сохраняет объект в БД"""
	print("Для регистрации введите свои данные:")
	first_name = input("Введите имя: ")
	last_name = input("Введите фамилию: ")
	email = input("Введите свой адрес электронной почты: ")

	gen = input("Укажите пол. 1 - мужской, 2 - женский: ")
	if gen == "1":
		gender = "Male"
	elif gen == "2":
		gender = "Female"
	else:
		print("Некорректно указан пол, присвоено значение unknown")
		gender = "unknown"

	birthdate = input("Введите дату рождения в формате YYYY-MM-DD: ")

	#Заведем рост, столбец REAL поэтому будем преобразовывать во float. Если пользователь укажет в значении ",", 
	#заменим на "."
	h = input("Укажите свой рост в метрах: ")
	if "," in h:
		h = h.replace(",", ".")
	height = float(h)

	#Конструируем объект пользователя User
	user = User(
		first_name = first_name,
		last_name = last_name,
		email = email,
		gender = gender,
		birthdate = birthdate,
		height = height
		)
	return user

def valid_input():
	"""фукнция проверяет корректность введенных данных"""
	pass

def find_athlete(session):
	"""Найдет пользователей по заданному критерию"""
	#Получаем id пользователя
	search_user_id = input("Введите id пользователя: ")

	#Ищем пользователя по id
	#Методом first возвращаем первый найденный объект типа query, т.к. используем поиск по id значит совпадение или одно или совпадений нет
	search_user = session.query(User).filter(User.id == int(search_user_id)).first()

	# Промежуточная переменная со значением +бесконечность для определения разниц в росте и датах рождения
	current_delta_date = float("inf")
	current_delta_height = float("inf")

	#Если пользователь найден
	if search_user:
		#Получаем год, месяц и день рождения найденного пользователя
		birth_user_year, birth_user_month, birth_user_day = search_user.birthdate.split("-")

		#Преобразуем дату рождения пользователя в формат подходящий для работы с datetime.date
		#В месяце и дне убираем "0" в начале если он есть
		if birth_user_month[0] == "0":
			birth_user_month = birth_user_month[1:]
		if birth_user_day[0] == "0":
			birth_user_day = birth_user_day[1:]

		#Преобразуем в int
		birth_user_year = int(birth_user_year)
		birth_user_month = int(birth_user_month)
		birth_user_day = int(birth_user_day)

		#Получаем дату рождения пользователя
		user_birthdate = datetime.date(birth_user_year, birth_user_month, birth_user_day)

		#Получаем список всех атлетов
		atheletes = session.query(Athelete).all()

		#Проходим по списку атлетов
		for athelete in atheletes:
			#Приводим день рождения атлета по аналогии c пользователем
			#Получаем год, месяц и день рождения каждого атлета
			birth_athelete_year, birth_athelete_month, birth_athelete_day = athelete.birthdate.split("-")

			#В месяце и дне убираем "0" в начале если он есть
			if birth_athelete_month[0] == "0":
				birth_athelete_month = birth_athelete_month[1:]
			if birth_athelete_day[0] == "0":
				birth_athelete_day = birth_athelete_day[1:]

			#Преобразуем в int
			birth_athelete_year = int(birth_athelete_year)
			birth_athelete_month = int(birth_athelete_month)
			birth_athelete_day = int(birth_athelete_day)

			#Получаем дату рождения атлета
			athelete_birthdate = datetime.date(birth_athelete_year, birth_athelete_month, birth_athelete_day)

			#Получаем разницу дат рождения в днях с помощью deltatime
			delta_days = abs((athelete_birthdate - user_birthdate).days)			

			#Если разница в днях меньше чем текущая
			if delta_days < current_delta_date:
				#Обновляем текущую разницу
				current_delta_date = delta_days
				#Сохраняем более ближайшего атлета
				similar_athelete_birth = athelete

			#Получаем разницу в росте между атлетом и пользователем, при этом проверяем на то, что данные о росте предоставлены
			if athelete.height is not None:
				delta_height = abs(float(athelete.height) - float(search_user.height))

				#Если разница между атлетом и пользователем меньше текущей разницы в росте:
				if delta_height < current_delta_height:
					#Обновляем текущую разницу
					current_delta_height = delta_height
					#Сохраняем более подходящего по росту атлета
					similar_athelete_height = athelete
		#Выводим на экран похожих атлетов
		print("Похожий по дате рождения атлет к пользователю родившемуся - ", search_user.birthdate, "|", "Разница в днях рождения: ", current_delta_date, "дней")
		print(similar_athelete_birth.id, similar_athelete_birth.name, similar_athelete_birth.birthdate)
			
		print("Ближайший по росту атлет к пользователю ростом - ", search_user.height, "м")
		print(similar_athelete_height.id, similar_athelete_height.name, similar_athelete_height.height, "м")

	else:
		print("Пользователь с таким id не существует")		

def main():
	"""Взаимодействует с пользователем, обрабатывает ввод"""
	session = connect_db() #Создаем объект сессии
	print("Выберете режим. 1 - регистрация нового пользователя, 2 - поиск атлета похожего на пользователя по ДР и росту")
	mode = input("Введите режим: ")
	if mode == "1":
		#Запрос данных пользователя
		user = request_data()
		#Добавляем нового пользователя
		session.add(user)
		#Сохраняем в БД
		session.commit()
		print("Новый пользователь сохранен")
	elif mode == "2":
		#Запускаем функцию поиска атлета
		find_athlete(session)
	else:
		#Тут комментарии излишни, введен некорректный режим работы программы.
		print("Некорретный режим")

if __name__ == "__main__":
	main()