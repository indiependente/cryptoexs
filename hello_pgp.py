import sys
import gnupg

def symmetric_decrypt(encfile, passphrase):
	gpg = gnupg.GPG()
	with open(encfile, 'rb') as f:
		status = gpg.decrypt_file(f, passphrase=passphrase, output='my-decrypted.txt')
		return status

def print_status(status):
	print 'status.ok =', status.ok
	print 'status.status =', status.status
	print 'status.stderr =', status.stderr

def print_decrypted(filename):
	with(open(filename, 'r')) as f:
		print f.read()

def main(encfile, passphrase):
	if passphrase is not None:
		print 'Decrypting using provided passphrase:', passphrase
		status = symmetric_decrypt(encfile, passphrase)
		print_status(status)
	else:
		print 'Decrypting using passphrases list'
		with open('words_alpha.txt', 'r') as words:
			for i, line in enumerate(words):
				print 'Trying with:', line.rstrip()
				status = symmetric_decrypt(encfile, line.rstrip())
				if status.ok:
					print 'DECRYPTION COMPLETE ---', i, 'steps needed'
					print_status(status)
					print '===== DECRYPTED FILE CONTENT ====='
					print_decrypted('my-decrypted.txt')
					break
			else:
				print '+++ NO PASSPHRASE MATCHING +++'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		exit('Usage: python hello_pgp.py <encryptedfile> [passphrase]')

	encfile = sys.argv[1]
	passphrase = None
	if len(sys.argv) == 3:
		passphrase = sys.argv[2]

	main(encfile, passphrase)