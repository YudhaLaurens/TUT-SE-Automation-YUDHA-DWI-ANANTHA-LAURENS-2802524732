import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class TestHerokuApp:
    """
    Feature: Login pada Aplikasi The Internet Heroku
      Sebagai pengguna aplikasi
      Saya ingin dapat login ke sistem
      Agar saya dapat mengakses area yang aman

    URL: https://the-internet.herokuapp.com/login
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup: Inisialisasi browser sebelum setiap tes"""
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, 10)
        yield
        # Teardown: Menutup browser setelah tes selesai
        self.driver.quit()

    def _save_screenshot(self, filename: str):
        """Helper: Menyimpan screenshot ke folder screenshots/"""
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        self.driver.save_screenshot(f"screenshots/{filename}")

    # ---------------------------------------------------------------
    # Scenario 1: Login dengan Username Benar dan Password Benar
    # ---------------------------------------------------------------
    def test_login_success(self):
        """
        Scenario: Login berhasil dengan kredensial yang valid
          Given saya berada di halaman login
          When saya memasukkan username "tomsmith"
          And saya memasukkan password "SuperSecretPassword!"
          And saya menekan tombol login
          Then saya melihat pesan "You logged into a secure area!"
        """

        # Given: Buka halaman login
        self.driver.get("https://the-internet.herokuapp.com/login")

        # When: Isi username
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")

        # And: Isi password yang benar
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")

        # And: Klik tombol login
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Then: Validasi pesan sukses
        flash_message = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        ).text
        assert "You logged into a secure area!" in flash_message, (
            f"Pesan sukses tidak ditemukan. Pesan aktual: {flash_message}"
        )

        # Simpan Screenshot
        self._save_screenshot("login_success.png")

    # ---------------------------------------------------------------
    # Scenario 2: Login dengan Username Benar dan Password Salah
    # ---------------------------------------------------------------
    def test_login_invalid_password(self):
        """
        Scenario: Login gagal dengan password yang tidak valid
          Given saya berada di halaman login
          When saya memasukkan username "tomsmith"
          And saya memasukkan password yang salah "WrongPassword!"
          And saya menekan tombol login
          Then saya melihat pesan "Your password is invalid!"
        """

        # Given: Buka halaman login
        self.driver.get("https://the-internet.herokuapp.com/login")

        # When: Isi username yang benar
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")

        # And: Isi password yang salah
        self.driver.find_element(By.ID, "password").send_keys("WrongPassword!")

        # And: Klik tombol login
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Then: Validasi pesan error
        flash_message = self.wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        ).text
        assert "Your password is invalid!" in flash_message, (
            f"Pesan error tidak ditemukan. Pesan aktual: {flash_message}"
        )

        # Simpan Screenshot
        self._save_screenshot("login_invalid_password.png")
